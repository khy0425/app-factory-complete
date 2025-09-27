# Templates Directory

이 디렉토리의 파일들은 **템플릿 파일**입니다.

## 중요 사항

- ⚠️ **IDE 오류 정상**: 이 파일들은 Flutter 프로젝트 컨텍스트 밖에 있어서 오류가 나타나는 것이 정상입니다
- 🔧 **플레이스홀더 포함**: `{{APP_NAME}}`, `{{CHANNEL_NAME}}` 등이 실제 앱 생성 시 대체됩니다
- 📝 **분석 무시**: `.analysis_options.yaml`과 `ignore_for_file` 주석으로 오류를 무시하도록 설정했습니다

## 템플릿 파일들

- `notification_service_template.dart.template` - 알림 서비스 템플릿
- `universal_level_system_template.dart.template` - 범용 레벨 선택 시스템 템플릿

⚠️ **중요**: 파일 확장자를 `.dart.template`로 변경하여 Dart 분석기가 오류를 표시하지 않도록 했습니다.

## 사용 방법

이 템플릿들은 앱 생성기에 의해 실제 Flutter 프로젝트로 복사되어 사용됩니다.
직접 편집하지 마세요.