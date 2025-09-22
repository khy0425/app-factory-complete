# 새로운 앱 생성 스크립트
param(
    [Parameter(Mandatory=$true)]
    [string]$AppName,
    
    [Parameter(Mandatory=$true)]
    [string]$PackageName,
    
    [Parameter(Mandatory=$false)]
    [string]$ConfigTemplate = "timer_app_template.json",
    
    [Parameter(Mandatory=$false)]
    [string]$Version = "1.0.0",
    
    [Parameter(Mandatory=$false)]
    [string]$Description = "",
    
    [Parameter(Mandatory=$false)]
    [string]$Author = "App Factory Team"
)

Write-Host "🏭 앱 공장: 새로운 앱 생성 시작..." -ForegroundColor Green
Write-Host "📱 앱 이름: $AppName" -ForegroundColor Cyan
Write-Host "📦 패키지 이름: $PackageName" -ForegroundColor Cyan

# 1. 새로운 프로젝트 디렉토리 생성
$projectDir = "../${AppName}_app"
$cleanAppName = $AppName.ToLower() -replace '\s+', '_'

Write-Host "📁 프로젝트 디렉토리 생성: $projectDir" -ForegroundColor Yellow

if (Test-Path $projectDir) {
    Write-Host "⚠️  디렉토리가 이미 존재합니다. 덮어쓰시겠습니까? (y/n)" -ForegroundColor Red
    $confirm = Read-Host
    if ($confirm -ne "y" -and $confirm -ne "Y") {
        Write-Host "❌ 작업이 취소되었습니다." -ForegroundColor Red
        exit
    }
    Remove-Item -Path $projectDir -Recurse -Force
}

# 2. Flutter 프로젝트 생성
Write-Host "🔧 Flutter 프로젝트 생성 중..." -ForegroundColor Yellow
flutter create --org com.appfactory $cleanAppName
Move-Item $cleanAppName $projectDir

# 3. 현재 프로젝트의 코어 파일들 복사
Write-Host "📋 코어 엔진 파일 복사 중..." -ForegroundColor Yellow

# lib 디렉토리 구조 생성
New-Item -ItemType Directory -Path "$projectDir/lib/core" -Force | Out-Null
New-Item -ItemType Directory -Path "$projectDir/lib/core/auth" -Force | Out-Null
New-Item -ItemType Directory -Path "$projectDir/lib/core/payment" -Force | Out-Null
New-Item -ItemType Directory -Path "$projectDir/lib/core/ads" -Force | Out-Null
New-Item -ItemType Directory -Path "$projectDir/lib/core/analytics" -Force | Out-Null
New-Item -ItemType Directory -Path "$projectDir/lib/core/common" -Force | Out-Null
New-Item -ItemType Directory -Path "$projectDir/lib/config" -Force | Out-Null
New-Item -ItemType Directory -Path "$projectDir/lib/config/themes" -Force | Out-Null

# 코어 파일들 복사
Copy-Item -Path "lib/core/*" -Destination "$projectDir/lib/core/" -Recurse -Force
Copy-Item -Path "lib/config/*" -Destination "$projectDir/lib/config/" -Recurse -Force

# assets 디렉토리 생성 및 설정 파일 복사
New-Item -ItemType Directory -Path "$projectDir/assets/config" -Force | Out-Null

# 4. 설정 파일 생성 (템플릿 기반)
Write-Host "⚙️  앱별 설정 파일 생성 중..." -ForegroundColor Yellow

$templatePath = "assets/config/$ConfigTemplate"
if (Test-Path $templatePath) {
    $configContent = Get-Content $templatePath -Raw | ConvertFrom-Json
    
    # 앱 정보 업데이트
    $configContent.app.name = $AppName
    $configContent.app.package_name = $PackageName
    $configContent.app.version = $Version
    if ($Description -ne "") {
        $configContent.app.description = $Description
    }
    if ($Author -ne "") {
        $configContent.app.author = $Author
    }
    
    # 새로운 설정 파일로 저장
    $configContent | ConvertTo-Json -Depth 10 | Set-Content "$projectDir/assets/config/app_config.json" -Encoding UTF8
    Write-Host "✅ 설정 파일 생성 완료" -ForegroundColor Green
} else {
    Write-Host "❌ 템플릿 파일을 찾을 수 없습니다: $templatePath" -ForegroundColor Red
    exit
}

# 5. pubspec.yaml 업데이트
Write-Host "📝 pubspec.yaml 업데이트 중..." -ForegroundColor Yellow

$pubspecPath = "$projectDir/pubspec.yaml"
$pubspecContent = Get-Content $pubspecPath -Raw

# 앱 이름과 설명 업데이트
$pubspecContent = $pubspecContent -replace "name: $cleanAppName", "name: $cleanAppName"
$pubspecContent = $pubspecContent -replace "description: .*", "description: `"$Description`""

# 의존성 추가
$dependencies = @"

  # Core dependencies for app factory
  provider: ^6.1.1
  shared_preferences: ^2.2.2
  path_provider: ^2.1.1
  google_mobile_ads: ^5.3.0
  
"@

$pubspecContent = $pubspecContent -replace "(dependencies:\s*\n\s*flutter:\s*\n\s*sdk: flutter)", "`$1$dependencies"

# assets 추가
$assetsSection = @"

  assets:
    - assets/config/
"@

$pubspecContent = $pubspecContent -replace "(uses-material-design: true)", "`$1$assetsSection"

Set-Content -Path $pubspecPath -Value $pubspecContent -Encoding UTF8

# 6. main.dart 생성
Write-Host "🎯 main.dart 생성 중..." -ForegroundColor Yellow

$mainDartContent = @"
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'core/app_factory.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  
  // 앱 팩토리 초기화
  await AppFactory.instance.initialize();
  
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: AppFactory.instance.getAppTitle(),
      theme: AppFactory.instance.createTheme(),
      home: MyHomePage(),
    );
  }
}

class MyHomePage extends StatefulWidget {
  @override
  _MyHomePageState createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(AppFactory.instance.getAppTitle()),
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: <Widget>[
            Text(
              '${AppFactory.instance.getAppTitle()}에 오신 것을 환영합니다!',
              style: Theme.of(context).textTheme.headlineSmall,
              textAlign: TextAlign.center,
            ),
            SizedBox(height: 20),
            Text(
              '버전: ${AppFactory.instance.getVersion()}',
              style: Theme.of(context).textTheme.bodyMedium,
            ),
            SizedBox(height: 20),
            _buildFeatureStatus('타이머', 'timer'),
            _buildFeatureStatus('습관 추적', 'habit_tracking'),
            _buildFeatureStatus('통계', 'statistics'),
            _buildFeatureStatus('업적', 'achievements'),
          ],
        ),
      ),
    );
  }

  Widget _buildFeatureStatus(String name, String feature) {
    final isEnabled = AppFactory.instance.isFeatureEnabled(feature);
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 4.0),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Icon(
            isEnabled ? Icons.check_circle : Icons.cancel,
            color: isEnabled ? Colors.green : Colors.red,
          ),
          SizedBox(width: 8),
          Text('$name: ${isEnabled ? "활성화" : "비활성화"}'),
        ],
      ),
    );
  }
}
"@

Set-Content -Path "$projectDir/lib/main.dart" -Value $mainDartContent -Encoding UTF8

# 7. 의존성 설치
Write-Host "📦 의존성 설치 중..." -ForegroundColor Yellow
Set-Location $projectDir
flutter pub get

# 8. 완료 메시지
Write-Host "" -ForegroundColor Green
Write-Host "🎉 새로운 앱 생성 완료!" -ForegroundColor Green
Write-Host "📍 프로젝트 경로: $((Get-Location).Path)" -ForegroundColor Cyan
Write-Host "🚀 실행 방법: flutter run" -ForegroundColor Cyan
Write-Host "" -ForegroundColor Green
Write-Host "📋 다음 단계:" -ForegroundColor Yellow
Write-Host "  1. 광고 ID 설정 (assets/config/app_config.json)" -ForegroundColor White
Write-Host "  2. 앱 아이콘 교체" -ForegroundColor White
Write-Host "  3. 기능별 화면 구현" -ForegroundColor White
Write-Host "  4. 테스트 및 빌드" -ForegroundColor White

Set-Location ..
"@
