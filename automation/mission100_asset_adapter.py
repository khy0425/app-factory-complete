#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Mission100 Asset Adapter
Mission: 100 프로젝트의 기존 에셋을 다른 운동 앱에 재활용하는 어댑터
"""

import os
import json
import shutil
from pathlib import Path
from typing import Dict, List, Optional
import logging

class Mission100AssetAdapter:
    """Mission: 100 에셋을 다른 운동 앱에 재활용하는 어댑터"""

    def __init__(self, mission100_path: str = "E:\\Projects\\Flutter\\misson100_version_2"):
        self.logger = logging.getLogger(__name__)
        self.mission100_path = Path(mission100_path)
        self.assets_path = self.mission100_path / "assets"

        # 재활용 가능한 에셋 매핑
        self.reusable_assets = {
            "character_images": {
                "기본차드.jpg": "character_base.jpg",
                "눈빔차드.jpg": "character_focused.jpg",
                "더블차드.jpg": "character_strong.jpg",
                "수면모자차드.jpg": "character_rest.jpg",
                "썬글차드.jpg": "character_cool.jpg",
                "정면차드.jpg": "character_front.jpg",
                "커피차드.png": "character_energy.png"
            },
            "app_icon": {
                "misson100_icon.png": "app_icon_base.png"
            }
        }

        # 기가차드 스타일 한국어 앱 컨셉
        self.chad_app_concepts = {
            "스쿼트차드": {
                "description": "200개? Yes. 30일 스쿼트 마스터 챌린지",
                "tagline": "스쿼트 한다... Yes.",
                "target_reps": 200,
                "exercise_type": "squat",
                "difficulty_levels": ["루키차드", "라이징차드", "알파차드", "기가차드"]
            },
            "플랭크차드": {
                "description": "5분? Yes. 코어 근력 끝판왕",
                "tagline": "플랭크 한다... Yes.",
                "target_time": 300,  # 5분
                "exercise_type": "plank",
                "difficulty_levels": ["코어루키", "코어파이터", "코어마스터", "코어킹"]
            },
            "버피차드": {
                "description": "100개? Yes. 전신운동 최강 챔피언",
                "tagline": "버피 한다... Yes.",
                "target_reps": 100,
                "exercise_type": "burpee",
                "difficulty_levels": ["버피비기너", "버피워리어", "버피비스트", "버피레전드"]
            },
            "홈트차드": {
                "description": "집에서? Yes. 홈트레이닝 올인원 마스터",
                "tagline": "홈트 한다... Yes.",
                "target_workouts": 30,
                "exercise_type": "home_workout",
                "difficulty_levels": ["홈트루키", "홈트파이터", "홈트마스터", "홈트킹"]
            }
        }

        # 운동별 캐릭터 매핑 (기가차드 스타일 메시지 포함)
        self.exercise_character_mapping = {
            "squat": {
                "beginner": {"image": "character_base.jpg", "message": "시작한다... Yes."},
                "intermediate": {"image": "character_focused.jpg", "message": "집중한다... Yes."},
                "advanced": {"image": "character_strong.jpg", "message": "강해진다... Yes."},
                "master": {"image": "character_cool.jpg", "message": "완벽하다... Yes."},
                "achievement": {"image": "character_front.jpg", "message": "달성했다... Yes."},
                "rest": {"image": "character_rest.jpg", "message": "휴식한다... Yes."},
                "energy": {"image": "character_energy.png", "message": "에너지... Yes."}
            },
            "plank": {
                "beginner": {"image": "character_base.jpg", "message": "시작한다... Yes."},
                "focused": {"image": "character_focused.jpg", "message": "집중한다... Yes."},
                "strong": {"image": "character_strong.jpg", "message": "버틴다... Yes."},
                "master": {"image": "character_cool.jpg", "message": "완벽하다... Yes."},
                "achievement": {"image": "character_front.jpg", "message": "달성했다... Yes."},
                "rest": {"image": "character_rest.jpg", "message": "휴식한다... Yes."}
            },
            "burpee": {
                "starter": {"image": "character_base.jpg", "message": "시작한다... Yes."},
                "warrior": {"image": "character_focused.jpg", "message": "전사다... Yes."},
                "beast": {"image": "character_strong.jpg", "message": "야수다... Yes."},
                "legend": {"image": "character_cool.jpg", "message": "전설이다... Yes."},
                "champion": {"image": "character_front.jpg", "message": "챔피언... Yes."},
                "recovery": {"image": "character_rest.jpg", "message": "회복한다... Yes."}
            },
            "home_workout": {
                "rookie": {"image": "character_base.jpg", "message": "홈트 시작... Yes."},
                "fighter": {"image": "character_focused.jpg", "message": "홈트 파이터... Yes."},
                "master": {"image": "character_strong.jpg", "message": "홈트 마스터... Yes."},
                "king": {"image": "character_cool.jpg", "message": "홈트 킹... Yes."},
                "achievement": {"image": "character_front.jpg", "message": "홈트 완료... Yes."},
                "rest": {"image": "character_rest.jpg", "message": "홈트 휴식... Yes."}
            }
        }

        self.logger.info(f"🎨 Mission100 Asset Adapter 초기화: {self.mission100_path}")

    def get_random_chad_app_concept(self) -> Dict:
        """랜덤한 기가차드 앱 컨셉 선택"""
        import random

        app_names = list(self.chad_app_concepts.keys())
        selected_name = random.choice(app_names)
        concept = self.chad_app_concepts[selected_name].copy()
        concept["app_name"] = selected_name

        self.logger.info(f"🎯 선택된 앱: {selected_name} - {concept['tagline']}")
        return concept

    def generate_chad_app_spec(self, app_concept: Dict) -> Dict:
        """기가차드 앱 상세 스펙 생성"""

        app_name = app_concept["app_name"]
        exercise_type = app_concept["exercise_type"]

        return {
            "app_name": app_name,
            "package_name": f"com.reaf.{exercise_type}",
            "display_name": app_name,
            "description": app_concept["description"],
            "tagline": app_concept["tagline"],
            "category": "Health & Fitness",
            "target_audience": "운동 초보자부터 고수까지",
            "key_features": [
                f"{exercise_type.upper()} 전문 프로그램",
                "기가차드 캐릭터 진화 시스템",
                "한국어 맞춤 운동 가이드",
                "일일 챌린지 및 업적 시스템",
                "진행률 추적 및 통계",
                "오프라인 모드 지원",
                "광고 기반 무료 앱"
            ],
            "monetization": {
                "model": "Freemium + Ads",
                "premium_features": [
                    "광고 제거",
                    "모든 차드 캐릭터 언락",
                    "고급 통계 및 분석",
                    "맞춤형 운동 플랜"
                ],
                "expected_revenue": "$1000-3000/month"
            },
            "technical_specs": {
                "platform": "Flutter (Android 우선, iOS 추후)",
                "target_platform": "Android",
                "storage": "SQLite + SharedPreferences",
                "offline_support": True,
                "push_notifications": True,
                "analytics": "Firebase Analytics",
                "min_sdk": 21,  # Android 5.0+
                "target_sdk": 34,  # Android 14
                "google_play_ready": True
            },
            "ui_theme": self.generate_theme_config(exercise_type),
            "character_mapping": self.exercise_character_mapping[exercise_type],
            "difficulty_levels": app_concept["difficulty_levels"]
        }

    def get_exercise_guide_template(self, exercise_type: str) -> Dict:
        """운동별 가이드 템플릿 생성"""

        templates = {
            "squat": {
                "formSteps": [
                    {
                        "stepNumber": 1,
                        "title": "시작 자세",
                        "description": "발을 어깨 너비로 벌리고 똑바로 서서 시작합니다.",
                        "keyPoints": [
                            "발은 어깨 너비로 벌림",
                            "발끝은 약간 바깥쪽으로",
                            "가슴을 쭉 펴고 시선은 정면",
                            "코어 근육 긴장"
                        ]
                    },
                    {
                        "stepNumber": 2,
                        "title": "하강 동작",
                        "description": "의자에 앉듯이 엉덩이를 뒤로 빼며 무릎을 구부립니다.",
                        "keyPoints": [
                            "무릎이 발끝을 넘지 않게",
                            "허벅지가 바닥과 평행할 때까지",
                            "등은 곧게 유지",
                            "체중은 뒤꿈치에"
                        ]
                    },
                    {
                        "stepNumber": 3,
                        "title": "상승 동작",
                        "description": "뒤꿈치로 바닥을 밀며 원래 자세로 돌아옵니다.",
                        "keyPoints": [
                            "뒤꿈치로 힘을 주어 상승",
                            "무릎과 엉덩이 동시에 펴기",
                            "상승하면서 숨 내쉬기",
                            "완전히 일어설 때까지"
                        ]
                    }
                ]
            },

            "plank": {
                "formSteps": [
                    {
                        "stepNumber": 1,
                        "title": "시작 자세",
                        "description": "팔꿈치와 발끝으로 몸을 지탱하는 플랭크 자세를 취합니다.",
                        "keyPoints": [
                            "팔꿈치는 어깨 바로 아래",
                            "몸은 머리부터 발뒤꿈치까지 일직선",
                            "복부와 둔부 근육 긴장",
                            "자연스럽게 호흡"
                        ]
                    },
                    {
                        "stepNumber": 2,
                        "title": "유지 동작",
                        "description": "올바른 자세를 유지하며 정해진 시간 동안 버팁니다.",
                        "keyPoints": [
                            "엉덩이가 처지지 않게",
                            "머리는 자연스럽게",
                            "무릎이 바닥에 닿지 않게",
                            "꾸준한 호흡 유지"
                        ]
                    }
                ]
            },

            "burpee": {
                "formSteps": [
                    {
                        "stepNumber": 1,
                        "title": "스쿼트 자세",
                        "description": "스쿼트 자세로 앉아 손을 바닥에 짚습니다.",
                        "keyPoints": [
                            "발은 어깨 너비로",
                            "손은 발 앞쪽 바닥에",
                            "무릎은 가슴 쪽으로",
                            "균형 잡기"
                        ]
                    },
                    {
                        "stepNumber": 2,
                        "title": "플랭크 점프",
                        "description": "다리를 뒤로 점프하여 플랭크 자세를 만듭니다.",
                        "keyPoints": [
                            "빠르게 다리를 뒤로",
                            "플랭크 자세 완성",
                            "코어 근육 긴장",
                            "팔은 곧게 유지"
                        ]
                    },
                    {
                        "stepNumber": 3,
                        "title": "푸쉬업 (선택)",
                        "description": "플랭크 자세에서 푸쉬업을 실행합니다.",
                        "keyPoints": [
                            "가슴이 바닥에 닿을 때까지",
                            "팔꿈치는 몸쪽으로",
                            "몸은 일직선 유지",
                            "강하게 밀어올리기"
                        ]
                    },
                    {
                        "stepNumber": 4,
                        "title": "점프업",
                        "description": "스쿼트 자세로 돌아와 위로 점프합니다.",
                        "keyPoints": [
                            "발을 가슴 쪽으로 당기기",
                            "스쿼트 자세에서 폭발적으로",
                            "팔을 위로 뻗으며 점프",
                            "부드럽게 착지"
                        ]
                    }
                ]
            }
        }

        return templates.get(exercise_type, templates["squat"])

    def copy_assets_for_app(self, target_app_dir: Path, exercise_type: str = "squat") -> Dict:
        """앱 디렉토리로 에셋 복사"""

        if not self.assets_path.exists():
            self.logger.error(f"❌ Mission100 assets not found: {self.assets_path}")
            return {"success": False, "error": "Source assets not found"}

        # 타겟 디렉토리 생성
        target_assets_dir = target_app_dir / "assets"
        target_images_dir = target_assets_dir / "images"
        target_data_dir = target_assets_dir / "data"
        target_icon_dir = target_assets_dir / "icon"

        for dir_path in [target_assets_dir, target_images_dir, target_data_dir, target_icon_dir]:
            dir_path.mkdir(parents=True, exist_ok=True)

        copied_files = []

        try:
            # 캐릭터 이미지 복사
            source_images = self.assets_path / "images"
            for original_name, new_name in self.reusable_assets["character_images"].items():
                source_file = source_images / original_name
                if source_file.exists():
                    target_file = target_images_dir / new_name
                    shutil.copy2(source_file, target_file)
                    copied_files.append(str(target_file))
                    self.logger.info(f"📁 복사됨: {original_name} → {new_name}")

            # 앱 아이콘 복사
            source_icon = self.assets_path / "icon" / "misson100_icon.png"
            if source_icon.exists():
                target_icon = target_icon_dir / "app_icon_base.png"
                shutil.copy2(source_icon, target_icon)
                copied_files.append(str(target_icon))
                self.logger.info(f"🎯 아이콘 복사됨: {target_icon}")

            # 운동 가이드 JSON 생성
            guide_data = self.get_exercise_guide_template(exercise_type)
            guide_file = target_data_dir / f"{exercise_type}_form_guide.json"

            with open(guide_file, 'w', encoding='utf-8') as f:
                json.dump(guide_data, f, ensure_ascii=False, indent=2)
            copied_files.append(str(guide_file))
            self.logger.info(f"📝 가이드 생성됨: {guide_file}")

            # pubspec.yaml에 추가할 에셋 목록 생성
            asset_entries = []
            for file_path in copied_files:
                relative_path = str(Path(file_path).relative_to(target_app_dir))
                asset_entries.append(f"    - {relative_path}")

            return {
                "success": True,
                "copied_files": copied_files,
                "asset_entries": asset_entries,
                "character_mapping": self.exercise_character_mapping.get(exercise_type, {}),
                "exercise_type": exercise_type
            }

        except Exception as e:
            self.logger.error(f"❌ 에셋 복사 실패: {e}")
            return {"success": False, "error": str(e)}

    def get_flutter_widget_templates(self, exercise_type: str) -> Dict:
        """재사용 가능한 Flutter 위젯 템플릿"""

        return {
            "character_widget": f'''
class CharacterWidget extends StatelessWidget {{
  final String characterType;
  final double size;
  final String? message;

  const CharacterWidget({{
    Key? key,
    required this.characterType,
    this.size = 120.0,
    this.message,
  }}) : super(key: key);

  @override
  Widget build(BuildContext context) {{
    final characterImages = {{
      'beginner': 'assets/images/character_base.jpg',
      'intermediate': 'assets/images/character_focused.jpg',
      'advanced': 'assets/images/character_strong.jpg',
      'master': 'assets/images/character_cool.jpg',
      'achievement': 'assets/images/character_front.jpg',
      'rest': 'assets/images/character_rest.jpg',
      'energy': 'assets/images/character_energy.png',
    }};

    return Column(
      children: [
        Container(
          width: size,
          height: size,
          decoration: BoxDecoration(
            shape: BoxShape.circle,
            image: DecorationImage(
              image: AssetImage(characterImages[characterType] ?? characterImages['beginner']!),
              fit: BoxFit.cover,
            ),
            boxShadow: [
              BoxShadow(
                color: Colors.black26,
                blurRadius: 10,
                offset: Offset(0, 5),
              ),
            ],
          ),
        ),
        if (message != null) ...[
          SizedBox(height: 8),
          Container(
            padding: EdgeInsets.symmetric(horizontal: 12, vertical: 6),
            decoration: BoxDecoration(
              color: Theme.of(context).primaryColor,
              borderRadius: BorderRadius.circular(20),
            ),
            child: Text(
              message!,
              style: TextStyle(
                color: Colors.white,
                fontWeight: FontWeight.bold,
                fontSize: 12,
              ),
            ),
          ),
        ],
      ],
    );
  }}
}}
''',

            "progress_card": f'''
class {exercise_type.capitalize()}ProgressCard extends StatelessWidget {{
  final int currentLevel;
  final int targetReps;
  final int completedReps;
  final double progressPercentage;

  const {exercise_type.capitalize()}ProgressCard({{
    Key? key,
    required this.currentLevel,
    required this.targetReps,
    required this.completedReps,
    required this.progressPercentage,
  }}) : super(key: key);

  @override
  Widget build(BuildContext context) {{
    return Card(
      elevation: 8,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
      child: Container(
        padding: EdgeInsets.all(16),
        decoration: BoxDecoration(
          borderRadius: BorderRadius.circular(16),
          gradient: LinearGradient(
            colors: [Colors.blue.shade400, Colors.blue.shade600],
            begin: Alignment.topLeft,
            end: Alignment.bottomRight,
          ),
        ),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Text(
                  'Level $currentLevel',
                  style: TextStyle(
                    color: Colors.white,
                    fontSize: 20,
                    fontWeight: FontWeight.bold,
                  ),
                ),
                CharacterWidget(
                  characterType: _getCharacterType(currentLevel),
                  size: 40,
                ),
              ],
            ),
            SizedBox(height: 12),
            Text(
              '$completedReps / $targetReps {exercise_type}s',
              style: TextStyle(
                color: Colors.white70,
                fontSize: 16,
              ),
            ),
            SizedBox(height: 8),
            LinearProgressIndicator(
              value: progressPercentage / 100,
              backgroundColor: Colors.white30,
              valueColor: AlwaysStoppedAnimation<Color>(Colors.white),
            ),
            SizedBox(height: 4),
            Text(
              '${{progressPercentage.toStringAsFixed(1)}}% Complete',
              style: TextStyle(
                color: Colors.white70,
                fontSize: 12,
              ),
            ),
          ],
        ),
      ),
    );
  }}

  String _getCharacterType(int level) {{
    if (level <= 2) return 'beginner';
    if (level <= 4) return 'intermediate';
    if (level <= 6) return 'advanced';
    return 'master';
  }}
}}
'''
        }

    def generate_theme_config(self, exercise_type: str) -> Dict:
        """운동별 테마 설정"""

        theme_configs = {
            "squat": {
                "primary_color": "0xFF2196F3",  # Blue
                "accent_color": "0xFF03DAC6",   # Teal
                "gradient_colors": ["0xFF2196F3", "0xFF21CBF3"],
                "app_name": "Squat Master",
                "app_tagline": "0 to 200 Squats Challenge"
            },
            "plank": {
                "primary_color": "0xFF4CAF50",  # Green
                "accent_color": "0xFF8BC34A",   # Light Green
                "gradient_colors": ["0xFF4CAF50", "0xFF8BC34A"],
                "app_name": "Plank Champion",
                "app_tagline": "Ultimate Core Strength"
            },
            "burpee": {
                "primary_color": "0xFFFF5722",  # Deep Orange
                "accent_color": "0xFFFF9800",   # Orange
                "gradient_colors": ["0xFFFF5722", "0xFFFF9800"],
                "app_name": "Burpee Beast",
                "app_tagline": "Full Body Challenge"
            }
        }

        return theme_configs.get(exercise_type, theme_configs["squat"])