#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
한국 사용자를 위한 매력적인 앱 이름 전략
과학적 프로그램 + 한글 감성
"""

import json
from datetime import datetime

class KoreanNamingStrategy:
    def __init__(self):
        self.target_audience = "한국 피트니스/자기계발 관심층"

        # Mission100 분석 (이미 성공한 이름)
        self.mission100_success_factors = {
            "이름": "Mission100",
            "성공_요인": [
                "미션이라는 단어의 도전적 느낌",
                "100이라는 명확한 목표",
                "영어지만 쉽고 직관적",
                "게임같은 느낌"
            ]
        }

    def analyze_korean_naming_options(self):
        """한국 사용자를 위한 이름 옵션 분석"""

        squat_options = {
            "스쿼트백과": {
                "english": "SquatWiki",
                "package": "com.reaf.squatwiki",
                "appeal": "모든 스쿼트 지식이 담긴 백과사전",
                "target": "정보를 원하는 사용자",
                "score": 7
            },
            "스쿼트마스터": {
                "english": "SquatMaster",
                "package": "com.reaf.squatmaster",
                "appeal": "마스터가 되는 과정",
                "target": "성취욕구가 강한 사용자",
                "score": 8
            },
            "스쿼트100": {
                "english": "Squat100",
                "package": "com.reaf.squat100",
                "appeal": "Mission100과 시리즈 통일성",
                "target": "명확한 목표를 원하는 사용자",
                "score": 9
            },
            "스쿼트업": {
                "english": "SquatUp",
                "package": "com.reaf.squatup",
                "appeal": "레벨업, 업그레이드 느낌",
                "target": "게임 감성을 좋아하는 사용자",
                "score": 8
            },
            "스쿼트챌린지": {
                "english": "SquatChallenge",
                "package": "com.reaf.squatchallenge",
                "appeal": "도전과 성취의 즐거움",
                "target": "챌린지 문화에 익숙한 MZ세대",
                "score": 9
            },
            "완벽한스쿼트": {
                "english": "PerfectSquat",
                "package": "com.reaf.perfectsquat",
                "appeal": "과학적으로 완벽한 스쿼트 학습",
                "target": "정확한 자세를 원하는 사용자",
                "score": 8
            },
            "스쿼트PT": {
                "english": "SquatPT",
                "package": "com.reaf.squatpt",
                "appeal": "개인 트레이너 느낌",
                "target": "PT받는 느낌을 원하는 사용자",
                "score": 9
            }
        }

        runner_options = {
            "런닝100": {
                "english": "Running100",
                "package": "com.reaf.running100",
                "appeal": "Mission100과 시리즈 통일",
                "target": "목표 지향적 사용자",
                "score": 8
            },
            "런마스터": {
                "english": "RunMaster",
                "package": "com.reaf.runmaster",
                "appeal": "런닝 마스터가 되는 과정",
                "target": "전문가가 되고 싶은 사용자",
                "score": 8
            },
            "러닝메이트": {
                "english": "RunningMate",
                "package": "com.reaf.runningmate",
                "appeal": "함께 달리는 친구 느낌",
                "target": "동기부여가 필요한 사용자",
                "score": 9
            },
            "런투런": {
                "english": "RunToRun",
                "package": "com.reaf.runtorun",
                "appeal": "None to Run 프로그램 직접 반영",
                "target": "초보자",
                "score": 7
            },
            "런업": {
                "english": "RunUp",
                "package": "com.reaf.runup",
                "appeal": "레벨업, 실력 향상",
                "target": "게임 감성 선호 사용자",
                "score": 8
            },
            "12주런닝": {
                "english": "Run12Weeks",
                "package": "com.reaf.run12weeks",
                "appeal": "12주 프로그램 명확히 표현",
                "target": "체계적 프로그램 선호자",
                "score": 9
            },
            "런데이": {
                "english": "RunDay",
                "package": "com.reaf.runday",
                "appeal": "매일 달리는 일상",
                "target": "습관 형성 희망자",
                "score": 8
            },
            "런스타트": {
                "english": "RunStart",
                "package": "com.reaf.runstart",
                "appeal": "런닝 시작을 도와주는 앱",
                "target": "완전 초보자",
                "score": 9
            }
        }

        return squat_options, runner_options

    def recommend_best_korean_names(self):
        """한국 시장을 위한 최종 추천"""

        recommendations = {
            "squat_final": {
                "1순위": "스쿼트PT",
                "이유": [
                    "PT받는 느낌으로 프리미엄 인식",
                    "Scientific Reports 연구 기반 = 전문 PT",
                    "한국에서 PT 문화 매우 활성화",
                    "과학적이면서도 친근한 이미지",
                    "10단계 승급 = PT 레벨 시스템"
                ],
                "2순위": "스쿼트챌린지",
                "2순위_이유": "MZ세대 챌린지 문화와 부합"
            },
            "runner_final": {
                "1순위": "런스타트",
                "이유": [
                    "None to Run 컨셉 완벽 반영",
                    "초보자 타겟 명확",
                    "시작의 설렘과 도전 의미",
                    "12주 후 진짜 러너가 되는 여정",
                    "부상 없이 안전하게 시작"
                ],
                "2순위": "러닝메이트",
                "2순위_이유": "함께하는 느낌으로 동기부여"
            },
            "series_concept": {
                "브랜드": "피트니스 마스터 시리즈",
                "라인업": [
                    "Mission100 - 푸쉬업 미션",
                    "스쿼트PT - 과학적 스쿼트 PT",
                    "런스타트 - 12주 런닝 시작"
                ],
                "공통_마케팅": "과학적 연구 기반 + 전문가 프로그램"
            }
        }

        return recommendations

    def create_marketing_messages(self):
        """한국 마케팅 메시지 생성"""

        messages = {
            "스쿼트PT": {
                "메인": "헬스장 PT 안 받아도 완벽한 스쿼트 마스터",
                "서브": [
                    "2023년 최신 연구 기반 프로그램",
                    "무릎 안전한 4단계 진화 시스템",
                    "10만원 PT비 아끼고 무료로 전문가 되기"
                ],
                "타겟_감정": "PT비 아까워하는 사람들의 마음"
            },
            "런스타트": {
                "메인": "러닝 한번도 못해본 사람도 12주면 러너",
                "서브": [
                    "작심삼일 NO! 과학적 12주 프로그램",
                    "무릎 부상 걱정 없는 체계적 시작",
                    "매일 5분부터 시작하는 기적"
                ],
                "타겟_감정": "시작이 두려운 초보자의 마음"
            }
        }

        return messages

    def run_korean_naming_analysis(self):
        """한국 이름 전략 분석 실행"""

        print("🇰🇷 한국 사용자를 위한 앱 이름 전략")
        print("="*60)

        # 1. 옵션 분석
        squat_options, runner_options = self.analyze_korean_naming_options()

        print("\n🏋️ 스쿼트 앱 한글 이름 후보 (점수순):")
        sorted_squat = sorted(squat_options.items(),
                            key=lambda x: x[1]['score'], reverse=True)
        for name, info in sorted_squat[:3]:
            print(f"  {info['score']}점: {name} - {info['appeal']}")

        print("\n🏃 러닝 앱 한글 이름 후보 (점수순):")
        sorted_runner = sorted(runner_options.items(),
                             key=lambda x: x[1]['score'], reverse=True)
        for name, info in sorted_runner[:3]:
            print(f"  {info['score']}점: {name} - {info['appeal']}")

        # 2. 최종 추천
        recommendations = self.recommend_best_korean_names()

        print(f"\n🏆 최종 추천:")
        print(f"• 스쿼트 앱: {recommendations['squat_final']['1순위']}")
        for reason in recommendations['squat_final']['이유'][:2]:
            print(f"  - {reason}")

        print(f"\n• 러닝 앱: {recommendations['runner_final']['1순위']}")
        for reason in recommendations['runner_final']['이유'][:2]:
            print(f"  - {reason}")

        # 3. 마케팅 메시지
        messages = self.create_marketing_messages()

        print(f"\n💬 마케팅 메시지:")
        for app, msg in messages.items():
            print(f"\n{app}:")
            print(f"  \"{msg['메인']}\"")

        # 4. 결과 저장
        result = {
            "분석_시간": datetime.now().isoformat(),
            "스쿼트_옵션": squat_options,
            "러닝_옵션": runner_options,
            "최종_추천": recommendations,
            "마케팅_메시지": messages
        }

        with open("korean_naming_analysis.json", "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)

        # 5. 요약
        self.print_final_summary(recommendations)

        return result

    def print_final_summary(self, recommendations):
        """최종 요약"""

        print("\n" + "="*60)
        print("📱 한국 시장 최종 앱 이름 결정")
        print("="*60)

        print("\n✅ 최종 시리즈:")
        for app in recommendations['series_concept']['라인업']:
            print(f"  • {app}")

        print("\n🎯 핵심 전략:")
        print("  • Mission100: 이미 성공한 브랜드 유지")
        print("  • 스쿼트PT: PT 문화 활용한 프리미엄 포지셔닝")
        print("  • 런스타트: 초보자 친화적 네이밍")

        print("\n💡 예상 효과:")
        print("  • PT비 아끼려는 2030 직장인 타겟")
        print("  • 러닝 입문자들의 진입장벽 낮춤")
        print("  • 과학적 근거 + 한국적 감성 조화")

        print("\n📁 분석 결과: korean_naming_analysis.json")

        print("\n🚀 다음 단계:")
        print("  1. 스쿼트PT, 런스타트 최종 승인")
        print("  2. 앱 파일 및 패키지명 업데이트")
        print("  3. 한국 마케팅 메시지로 스토어 등록")

if __name__ == "__main__":
    naming = KoreanNamingStrategy()
    naming.run_korean_naming_analysis()