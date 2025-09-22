#!/bin/bash
# semsem_master AdMob 자동 적용 스크립트

echo "📱 semsem_master AdMob 설정 적용 중..."

# 1. AdMob Service 파일 복사
cp admob_setup/admob_service.dart ../flutter_apps/semsem_master/lib/services/

# 2. pubspec.yaml에 AdMob 의존성 추가
echo "  google_mobile_ads: ^5.1.0" >> ../flutter_apps/semsem_master/pubspec.yaml

# 3. Android Manifest 업데이트 필요 (수동)
echo "⚠️  Android Manifest에 App ID 추가가 필요합니다"
echo "📋 admob_setup_guide.md 파일을 참조하세요"

echo "✅ AdMob 설정 적용 완료!"
echo "🔗 다음 단계: admob_setup_guide.md 파일을 확인하여 실제 AdMob 계정을 설정하세요"
