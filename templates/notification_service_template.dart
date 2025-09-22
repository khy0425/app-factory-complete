import 'dart:async';
import 'dart:convert';
import 'dart:math';
import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_local_notifications/flutter_local_notifications.dart';
import 'package:permission_handler/permission_handler.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:timezone/timezone.dart' as tz;
import 'package:timezone/data/latest.dart' as tz;

/// {{APP_NAME}} 통합 알림 서비스
///
/// 개선된 권한 요청 시스템:
/// 1. 기본 알림 권한만 요청 → 바로 완료
/// 2. 정확한 알람 권한은 선택적으로 요청
/// 3. 완전한 폴백 시스템 (정확한 → 부정확한 → 즉시 알림)
class NotificationService {
  static final FlutterLocalNotificationsPlugin _notifications =
      FlutterLocalNotificationsPlugin();

  static bool _isInitialized = false;

  // Android 12+ SCHEDULE_EXACT_ALARM 권한 확인을 위한 MethodChannel
  static const MethodChannel _channel = MethodChannel('{{CHANNEL_NAME}}');

  /// Android 12+에서 SCHEDULE_EXACT_ALARM 권한이 있는지 확인
  static Future<bool> canScheduleExactAlarms() async {
    if (defaultTargetPlatform != TargetPlatform.android) {
      return true; // iOS는 권한 필요 없음
    }

    try {
      final bool? canSchedule = await _channel.invokeMethod('canScheduleExactAlarms');
      debugPrint('🔔 SCHEDULE_EXACT_ALARM 권한 상태: $canSchedule');
      return canSchedule ?? false;
    } on PlatformException catch (e) {
      debugPrint('❌ SCHEDULE_EXACT_ALARM 권한 확인 오류: ${e.message}');
      // Android 12 미만이면 true 반환 (권한 필요 없음)
      return true;
    }
  }

  /// Android 12+에서 SCHEDULE_EXACT_ALARM 권한 요청
  static Future<bool> requestExactAlarmPermission() async {
    if (defaultTargetPlatform != TargetPlatform.android) {
      return true; // iOS는 권한 필요 없음
    }

    try {
      debugPrint('🔔 SCHEDULE_EXACT_ALARM 권한 요청 시작...');
      final bool? granted = await _channel.invokeMethod('requestExactAlarmPermission');
      debugPrint('🔔 SCHEDULE_EXACT_ALARM 권한 요청 결과: $granted');

      // 설정 화면으로 이동한 후 충분한 시간 대기
      await Future.delayed(const Duration(seconds: 2));

      // 실제 권한 상태를 다시 확인 (사용자가 허용했는지 확인)
      final actualPermission = await canScheduleExactAlarms();
      debugPrint('🔔 SCHEDULE_EXACT_ALARM 실제 권한 상태: $actualPermission');

      return actualPermission;
    } on PlatformException catch (e) {
      debugPrint('❌ SCHEDULE_EXACT_ALARM 권한 요청 오류: ${e.message}');
      return false;
    } catch (e) {
      debugPrint('❌ SCHEDULE_EXACT_ALARM 권한 요청 일반 오류: $e');
      return false;
    }
  }

  /// 안전한 알림 스케줄링 (권한 확인 포함)
  static Future<bool> _safeScheduleNotification({
    required int id,
    required String title,
    required String body,
    required DateTime scheduledDate,
    required NotificationDetails notificationDetails,
  }) async {
    try {
      // Android 12+에서 정확한 알람 권한 확인
      if (defaultTargetPlatform == TargetPlatform.android) {
        final canSchedule = await canScheduleExactAlarms();

        if (!canSchedule) {
          debugPrint('⚠️ SCHEDULE_EXACT_ALARM 권한이 없어 부정확한 알림 방식 사용');
          // 권한이 없으면 부정확한 알림 스케줄링 사용
          return await scheduleInexactNotification(
            id: id,
            title: title,
            body: body,
            scheduledDate: scheduledDate,
            notificationDetails: notificationDetails,
          );
        }
      }

      // 권한이 있으면 정확한 시간에 스케줄링
      await _notifications.zonedSchedule(
        id,
        title,
        body,
        tz.TZDateTime.from(scheduledDate, tz.local),
        notificationDetails,
        uiLocalNotificationDateInterpretation:
            UILocalNotificationDateInterpretation.absoluteTime,
      );

      debugPrint('✅ 정확한 알림 스케줄링 성공: $title (${scheduledDate.toString()})');
      return true;
    } catch (e) {
      debugPrint('❌ 정확한 알림 스케줄링 실패: $e');

      // 실패 시 부정확한 알림으로 대체
      try {
        return await scheduleInexactNotification(
          id: id,
          title: title,
          body: body,
          scheduledDate: scheduledDate,
          notificationDetails: notificationDetails,
        );
      } catch (fallbackError) {
        debugPrint('❌ 부정확한 알림 대체도 실패: $fallbackError');

        // 최후 수단: 즉시 알림 표시
        try {
          await _notifications.show(id, title, body, notificationDetails);
          debugPrint('🔄 최후 수단으로 즉시 알림 표시');
          return false;
        } catch (immediateError) {
          debugPrint('❌ 즉시 알림도 실패: $immediateError');
          return false;
        }
      }
    }
  }

  /// 알림 서비스 초기화
  static Future<void> initialize() async {
    if (_isInitialized) return;

    // 타임존 초기화
    tz.initializeTimeZones();

    // Android 초기화 설정
    const AndroidInitializationSettings androidSettings =
        AndroidInitializationSettings('@mipmap/ic_launcher');

    // iOS 초기화 설정
    const DarwinInitializationSettings iosSettings =
        DarwinInitializationSettings(
      requestAlertPermission: true,
      requestBadgePermission: true,
      requestSoundPermission: true,
    );

    const InitializationSettings initSettings = InitializationSettings(
      android: androidSettings,
      iOS: iosSettings,
    );

    await _notifications.initialize(
      initSettings,
      onDidReceiveNotificationResponse: _onNotificationTapped,
    );

    _isInitialized = true;
  }

  /// 사용자 친화적 권한 요청 다이얼로그 표시
  static Future<bool> showPermissionRequestDialog(BuildContext context) async {
    if (!context.mounted) return false;

    // 현재 권한 상태 확인
    final hasNotificationPermission = await _hasNotificationPermission();
    final hasExactAlarmPermission = await canScheduleExactAlarms();

    // 기본 알림 권한만 있어도 작동하도록 변경
    if (hasNotificationPermission) {
      debugPrint('✅ 기본 알림 권한 있음 - 바로 진행');
      // 정확한 알람이 없어도 기본 알림으로 작동
      if (!hasExactAlarmPermission) {
        _showExactAlarmInfo(context);
      }
      return true;
    }

    // 권한 요청 다이얼로그 표시
    final shouldRequest = await showDialog<bool>(
      context: context,
      barrierDismissible: true, // 사용자가 취소할 수 있도록
      builder: (BuildContext context) {
        return AlertDialog(
          title: const Row(
            children: [
              Icon(Icons.security, color: Color(0xFF4DABF7)),
              SizedBox(width: 8),
              Text('🔥 {{APP_TITLE}} 알림 활성화! 🔥'),
            ],
          ),
          content: SingleChildScrollView(
            child: Column(
              mainAxisSize: MainAxisSize.min,
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                const Text(
                  '💪 CHAD 알림 활성화!\n바로 설정하자! FXXK THE EXCUSES! 💪',
                  style: TextStyle(fontSize: 16),
                ),
                const SizedBox(height: 16),

                if (!hasNotificationPermission)
                  const Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Row(
                        children: [
                          Icon(Icons.notifications, color: Colors.blue, size: 20),
                          SizedBox(width: 8),
                          Expanded(
                            child: Text(
                              '🔔 운동 알림 권한',
                              style: TextStyle(fontWeight: FontWeight.bold),
                            ),
                          ),
                        ],
                      ),
                      Padding(
                        padding: EdgeInsets.only(left: 28),
                        child: Text('매일 운동 시간 알림! 놓치면 WEAK! 💪'),
                      ),
                      SizedBox(height: 12),
                    ],
                  ),

                const SizedBox(height: 16),
                Container(
                  padding: const EdgeInsets.all(12),
                  decoration: BoxDecoration(
                    color: Colors.blue.withValues(alpha: 0.1),
                    borderRadius: BorderRadius.circular(8),
                  ),
                  child: const Text(
                    '💡 기본 알림만으로도 CHAD 될 수 있다!\n하지만 LEGENDARY CHAD는 모든 권한 허용! DOMINATION! 🚀',
                    style: TextStyle(
                      fontSize: 14,
                      color: Colors.blue,
                    ),
                  ),
                ),
              ],
            ),
          ),
          actions: [
            TextButton(
              onPressed: () => Navigator.of(context).pop(false),
              child: const Text(
                '나중에... (WEAK)',
                style: TextStyle(color: Colors.grey),
              ),
            ),
            ElevatedButton(
              onPressed: () => Navigator.of(context).pop(true),
              style: ElevatedButton.styleFrom(
                backgroundColor: Color(0xFF4DABF7),
                foregroundColor: Colors.white,
              ),
              child: const Text('🔥 CHAD 알림 켜기! 만삣삐!'),
            ),
          ],
        );
      },
    );

    if (shouldRequest != true) return false;

    // 실제 권한 요청 수행 (기본 알림만 우선)
    final basicGranted = await _requestBasicNotificationPermission();

    if (basicGranted) {
      // 기본 알림 권한이 있으면 성공으로 처리
      if (!hasExactAlarmPermission) {
        // 정확한 알람 권한은 선택적으로 요청
        _requestExactAlarmOptionally(context);
      }
      return true;
    }

    return false;
  }

  /// 기본 알림 권한만 요청 (사용자 친화적)
  static Future<bool> _requestBasicNotificationPermission() async {
    try {
      if (defaultTargetPlatform == TargetPlatform.android) {
        // Android - permission_handler 사용
        final status = await Permission.notification.request();
        final granted = status.isGranted;

        final prefs = await SharedPreferences.getInstance();
        await prefs.setBool('notification_permission_granted', granted);

        debugPrint('📱 Android 기본 알림 권한: $granted');
        return granted;
      } else if (defaultTargetPlatform == TargetPlatform.iOS) {
        // iOS - flutter_local_notifications 사용
        final granted = await _notifications
            .resolvePlatformSpecificImplementation<IOSFlutterLocalNotificationsPlugin>()
            ?.requestPermissions(
              alert: true,
              badge: true,
              sound: true,
            );

        final prefs = await SharedPreferences.getInstance();
        await prefs.setBool('notification_permission_granted', granted ?? false);

        debugPrint('🍎 iOS 기본 알림 권한: $granted');
        return granted ?? false;
      }
    } catch (e) {
      debugPrint('❌ 기본 알림 권한 요청 실패: $e');
    }

    return false;
  }

  /// 정확한 알람 권한을 선택적으로 요청
  static Future<void> _requestExactAlarmOptionally(BuildContext context) async {
    // 백그라운드에서 정확한 알람 권한 요청
    Future.delayed(const Duration(seconds: 1), () async {
      if (!context.mounted) return;

      final shouldRequest = await showDialog<bool>(
        context: context,
        barrierDismissible: true,
        builder: (BuildContext context) {
          return AlertDialog(
            title: const Text('⚡ LEGENDARY CHAD MODE 업그레이드! ⚡'),
            content: const Column(
              mainAxisSize: MainAxisSize.min,
              children: [
                Text(
                  '🔥 더 정확한 시간에 알림을 받고 싶다면\nLEGENDARY MODE를 활성화하자! 🔥',
                  textAlign: TextAlign.center,
                ),
                SizedBox(height: 16),
                Text(
                  '💡 지금 안 해도 괜찮다!\n나중에 설정에서 언제든지 가능! 만삣삐!',
                  style: TextStyle(fontSize: 14, color: Colors.grey),
                  textAlign: TextAlign.center,
                ),
              ],
            ),
            actions: [
              TextButton(
                onPressed: () => Navigator.of(context).pop(false),
                child: const Text('나중에 (BASIC CHAD)'),
              ),
              ElevatedButton(
                onPressed: () => Navigator.of(context).pop(true),
                style: ElevatedButton.styleFrom(
                  backgroundColor: const Color(0xFF4DABF7),
                  foregroundColor: Colors.white,
                ),
                child: const Text('⚡ LEGENDARY MODE ON! ⚡'),
              ),
            ],
          );
        },
      );

      if (shouldRequest == true) {
        await requestExactAlarmPermission();
      }
    });
  }

  /// 정확한 알람 권한 설명 토스트 표시
  static void _showExactAlarmInfo(BuildContext context) {
    // 간단한 정보 메시지 표시
    if (context.mounted) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text('💡 CHAD MODE 활성화! 더 정확한 알림은 나중에 설정 가능! 🔥'),
          duration: Duration(seconds: 3),
          backgroundColor: Colors.blue,
        ),
      );
    }
  }

  /// 기본 알림 권한이 있는지 확인
  static Future<bool> _hasNotificationPermission() async {
    await initialize();

    if (defaultTargetPlatform == TargetPlatform.android) {
      final androidPlugin = _notifications.resolvePlatformSpecificImplementation<
          AndroidFlutterLocalNotificationsPlugin>();

      if (androidPlugin != null) {
        // Android에서는 권한 상태를 직접 확인하기 어려우므로
        // SharedPreferences에 저장된 상태를 확인
        final prefs = await SharedPreferences.getInstance();
        return prefs.getBool('notification_permission_granted') ?? false;
      }
    }

    return true; // iOS는 기본적으로 true로 가정
  }

  /// 부정확한 알림 스케줄링 (SCHEDULE_EXACT_ALARM 권한이 없을 때 사용)
  static Future<bool> scheduleInexactNotification({
    required int id,
    required String title,
    required String body,
    required DateTime scheduledDate,
    required NotificationDetails notificationDetails,
  }) async {
    try {
      debugPrint('📅 부정확한 알림 스케줄링 시도: $title');

      // 예약 시간까지의 지연 시간 계산
      final now = DateTime.now();
      final delay = scheduledDate.difference(now);

      if (delay.isNegative) {
        // 과거 시간이면 즉시 표시
        await _notifications.show(id, title, body, notificationDetails);
        debugPrint('⚡ 과거 시간이므로 즉시 알림 표시');
        return true;
      }

      // 30분 이내면 정확한 스케줄링 시도 (시스템이 허용할 가능성 높음)
      if (delay.inMinutes <= 30) {
        try {
          await _notifications.zonedSchedule(
            id,
            title,
            body,
            tz.TZDateTime.from(scheduledDate, tz.local),
            notificationDetails,
            uiLocalNotificationDateInterpretation:
                UILocalNotificationDateInterpretation.absoluteTime,
          );
          debugPrint('✅ 30분 이내 정확한 스케줄링 성공');
          return true;
        } catch (e) {
          debugPrint('⚠️ 30분 이내 정확한 스케줄링 실패, 부정확한 방법 사용: $e');
        }
      }

      // 긴 지연시간의 경우 즉시 알림으로 대체
      await _notifications.show(id, title, body, notificationDetails);
      debugPrint('🔄 긴 지연시간으로 즉시 알림 표시');

      return true;
    } catch (e) {
      debugPrint('❌ 부정확한 알림 스케줄링 실패: $e');
      return false;
    }
  }

  /// 일일 운동 알림 설정
  static Future<void> scheduleDailyWorkoutReminder({
    required TimeOfDay time,
    String title = '🔥 WORKOUT TIME! 지금 당장! 만삣삐! 🔥',
    String body = '💪 {{APP_TITLE}} 운동 시간! LEGENDARY CHAD MODE 활성화! 💪',
  }) async {
    await initialize();

    // 기존 일일 알림 취소
    await _notifications.cancel(1);

    // 다음 7일간의 알림을 개별적으로 스케줄링
    final now = DateTime.now();

    for (int i = 0; i < 7; i++) {
      final targetDate = now.add(Duration(days: i));
      var scheduledDate = DateTime(
        targetDate.year,
        targetDate.month,
        targetDate.day,
        time.hour,
        time.minute,
      );

      // 오늘 시간이 이미 지났다면 내일부터 시작
      if (i == 0 && scheduledDate.isBefore(now)) {
        continue;
      }

      // 각 날짜별로 고유한 알림 ID 사용 (1000 + 일수)
      final notificationId = 1000 + i;

      await _safeScheduleNotification(
        id: notificationId,
        title: title,
        body: body,
        scheduledDate: scheduledDate,
        notificationDetails: NotificationDetails(
          android: AndroidNotificationDetails(
            'daily_workout',
            'Daily Workout Reminder',
            channelDescription: '매일 운동 알림',
            importance: Importance.max,
            priority: Priority.high,
            icon: '@mipmap/ic_launcher',
            sound: RawResourceAndroidNotificationSound('notification_sound'),
            playSound: true,
            enableVibration: true,
            vibrationPattern: Int64List.fromList([0, 1000, 500, 1000]),
          ),
          iOS: DarwinNotificationDetails(
            presentAlert: true,
            presentBadge: true,
            presentSound: true,
          ),
        ),
      );
    }

    // 설정된 시간 저장
    final prefs = await SharedPreferences.getInstance();
    await prefs.setInt('notification_hour', time.hour);
    await prefs.setInt('notification_minute', time.minute);
    await prefs.setBool('daily_notification_enabled', true);
  }

  /// 업적 달성 알림
  static Future<void> showAchievementNotification(
    String title,
    String description,
  ) async {
    await _safeScheduleNotification(
      id: 3, // 업적 알림 ID
      title: '🏆 ACHIEVEMENT UNLOCKED! 만삣삐! 🏆',
      body: '🔥 $title: $description FXXK YEAH! 🔥',
      scheduledDate: DateTime.now(),
      notificationDetails: NotificationDetails(
        android: AndroidNotificationDetails(
          'achievement',
          'Achievement Notifications',
          channelDescription: '업적 달성 알림',
          importance: Importance.high,
          priority: Priority.high,
          icon: '@mipmap/ic_launcher',
        ),
        iOS: DarwinNotificationDetails(
          presentAlert: true,
          presentBadge: true,
          presentSound: true,
        ),
      ),
    );
  }

  /// 운동 완료 축하 알림
  static Future<void> showWorkoutCompletionCelebration({
    required int totalReps,
    required double completionRate,
  }) async {
    await initialize();

    String title = '🔥 WORKOUT DEMOLISHED! 만삣삐! 🔥';
    String body = '$totalReps REPS DESTROYED! ${(completionRate * 100).toInt()}% DOMINATION! FXXK YEAH!';

    if (completionRate >= 1.0) {
      title = '🚀 PERFECT EXECUTION! LEGENDARY! 🚀';
      body = '100% TARGET ANNIHILATED! TRUE CHAD CONFIRMED! ULTRA BEAST MODE! 만삣삐! 💪';
    } else if (completionRate >= 0.8) {
      title = '⚡ EXCELLENT DESTRUCTION! GIGACHAD! ⚡';
      body = '목표의 ${(completionRate * 100).toInt()}% 달성! 차드의 길을 걷고 있습니다! 🔥';
    }

    await _safeScheduleNotification(
      id: 3, // 알림 ID
      title: title,
      body: body,
      scheduledDate: DateTime.now(),
      notificationDetails: NotificationDetails(
        android: AndroidNotificationDetails(
          'workout_completion',
          'Workout Completion',
          channelDescription: '운동 완료 축하 알림',
          importance: Importance.high,
          priority: Priority.high,
          icon: '@mipmap/ic_launcher',
        ),
        iOS: DarwinNotificationDetails(
          presentAlert: true,
          presentBadge: true,
          presentSound: true,
        ),
      ),
    );
  }

  /// 모든 알림 취소
  static Future<void> cancelAllNotifications() async {
    await _notifications.cancelAll();

    final prefs = await SharedPreferences.getInstance();
    await prefs.setBool('daily_notification_enabled', false);
  }

  /// 알림 탭 시 처리
  static void _onNotificationTapped(NotificationResponse response) {
    debugPrint('알림 탭됨: ${response.payload}');
    // 필요시 특정 화면으로 네비게이션 처리
  }

  /// 알림 권한이 있는지 확인 (기존 호환성 메소드)
  static Future<bool> hasPermission() async {
    try {
      final hasBasicPermission = await _hasNotificationPermission();
      final hasExactAlarms = await canScheduleExactAlarms();

      // 기본 알림만 있어도 충분하다고 판단
      return hasBasicPermission;
    } catch (e) {
      debugPrint('권한 확인 오류: $e');
      return false;
    }
  }
}