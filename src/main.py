"""
재난·안전 체크리스트 시스템 - CLI 인터페이스
"""
import argparse
import sys
from pathlib import Path

# src 디렉토리를 Python 경로에 추가
sys.path.insert(0, str(Path(__file__).parent))

from utils.config import config
from checklist.templates import ChecklistTemplates, FacilityType, CheckPhase, FocusArea
from checklist.generator import ChecklistGenerator


def main():
    """메인 함수"""
    parser = argparse.ArgumentParser(
        description='재난·안전 체크리스트 시스템',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
사용 예시:
  # 기본 체크리스트 생성
  python src/main.py generate "서울시 강남구청" --type "지자체" --stage "정기 점검"

  # 데이터 수집 포함
  python src/main.py generate "○○건설 현장" --type "건설현장" --stage "초기 평가" --collect

  # JSON 형식으로 출력
  python src/main.py generate "△△제조공장" --type "제조사업장" --stage "연간 종합" --format json

  # 템플릿 목록 보기
  python src/main.py list
        """
    )

    subparsers = parser.add_subparsers(dest='command', help='실행할 명령')

    # generate 명령
    generate_parser = subparsers.add_parser('generate', help='체크리스트 생성')
    generate_parser.add_argument('keyword', help='시설/사업장 키워드 (예: "서울시 강남구청")')
    generate_parser.add_argument(
        '--type', '-t',
        choices=[ft.value for ft in FacilityType],
        default=FacilityType.OTHER.value,
        help='시설 유형'
    )
    generate_parser.add_argument(
        '--stage', '-s',
        choices=[cp.value for cp in CheckPhase],
        default=CheckPhase.INITIAL.value,
        help='점검 단계'
    )
    generate_parser.add_argument(
        '--focus', '-f',
        choices=[fa.value for fa in FocusArea],
        help='관심 영역'
    )
    generate_parser.add_argument(
        '--collect', '-c',
        action='store_true',
        help='리서치 데이터 수집 실행'
    )
    generate_parser.add_argument(
        '--format',
        choices=['markdown', 'json', 'both'],
        default='markdown',
        help='출력 형식'
    )
    generate_parser.add_argument(
        '--output', '-o',
        help='출력 파일 경로'
    )

    # list 명령
    list_parser = subparsers.add_parser('list', help='사용 가능한 템플릿 및 옵션 보기')
    list_parser.add_argument(
        '--category', '-c',
        help='특정 카테고리의 상세 정보'
    )

    # config 명령
    config_parser = subparsers.add_parser('config', help='설정 관리')
    config_parser.add_argument(
        '--show', '-s',
        action='store_true',
        help='현재 설정 보기'
    )
    config_parser.add_argument(
        '--set',
        nargs=2,
        metavar=('KEY', 'VALUE'),
        help='설정값 변경 (예: --set api_keys.github YOUR_TOKEN)'
    )

    args = parser.parse_args()

    if args.command == 'generate':
        cmd_generate(args)
    elif args.command == 'list':
        cmd_list(args)
    elif args.command == 'config':
        cmd_config(args)
    else:
        parser.print_help()


def cmd_generate(args):
    """체크리스트 생성 명령"""
    print(f"\n{'='*70}")
    print(f"  재난·안전 체크리스트 시스템")
    print(f"{'='*70}\n")

    # 생성기 초기화
    generator = ChecklistGenerator(config.settings)

    # 체크리스트 생성
    result = generator.generate(
        keyword=args.keyword,
        facility_type=args.type,
        check_phase=args.stage,
        focus_area=args.focus,
        collect_data=args.collect
    )

    # 출력
    if args.format in ['markdown', 'both']:
        output_path = args.output if args.output else None
        md_path = generator.export_to_markdown(result, output_path)
        print(f"\n✅ Markdown 파일: {md_path}")

    if args.format in ['json', 'both']:
        output_path = args.output if args.output and args.format == 'json' else None
        json_path = generator.export_to_json(result, output_path)
        print(f"✅ JSON 파일: {json_path}")

    # 요약 출력
    print(f"\n{'='*70}")
    print("📊 생성 요약")
    print(f"{'='*70}")

    summary = result['research_summary']
    print(f"- 웹 자료: {summary['web_sources']}건")
    print(f"- 논문: {summary['papers']}건")
    print(f"- 기술 프로젝트: {summary['tech_projects']}건")
    print(f"- API: {summary['apis']}건")
    print(f"- 총 리소스: {summary['total_resources']}건")

    if result['recommendations']:
        print(f"\n💡 추천 사항:")
        for rec in result['recommendations']:
            print(f"  {rec}")

    print(f"\n{'='*70}\n")


def cmd_list(args):
    """템플릿 목록 명령"""
    templates = ChecklistTemplates()

    if args.category:
        # 특정 카테고리 상세 정보
        category = templates.categories.get(args.category)
        if not category:
            print(f"❌ 카테고리를 찾을 수 없습니다: {args.category}")
            return

        questions = templates.templates.get(args.category, [])

        print(f"\n{category['icon']} {category['name']}")
        print(f"{'='*60}")
        print(f"{category['description']}\n")

        print(f"질문 ({len(questions)}개):")
        for i, q in enumerate(questions, 1):
            importance_badge = {
                'high': '🔴',
                'medium': '🟡',
                'low': '🟢'
            }.get(q['importance'], '')

            print(f"\n{i}. {q['question']} {importance_badge}")
            print(f"   유형: {q['type']}")
            print(f"   필수: {'예' if q['required'] else '아니오'}")
            if q.get('options'):
                print(f"   선택지: {', '.join(q['options'])}")

    else:
        # 전체 목록
        print("\n📋 사용 가능한 카테고리")
        print(f"{'='*60}")

        for cat_id, cat_info in templates.categories.items():
            questions_count = len(templates.templates.get(cat_id, []))
            print(f"{cat_info['icon']} {cat_info['name']}")
            print(f"   {cat_info['description']}")
            print(f"   질문 수: {questions_count}개")
            print()

        print("\n📌 시설 유형")
        print(f"{'='*60}")
        for ft in FacilityType:
            print(f"  - {ft.value}")

        print("\n📌 점검 단계")
        print(f"{'='*60}")
        for cp in CheckPhase:
            print(f"  - {cp.value}")

        print("\n📌 관심 영역")
        print(f"{'='*60}")
        for fa in FocusArea:
            print(f"  - {fa.value}")

        print()


def cmd_config(args):
    """설정 관리 명령"""
    if args.show:
        print("\n⚙️  현재 설정")
        print(f"{'='*60}")
        import json
        print(json.dumps(config.settings, indent=2, ensure_ascii=False))
        print()

    elif args.set:
        key, value = args.set
        config.set(key, value)
        config.save()
        print(f"✅ 설정 저장: {key} = {value}")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  사용자에 의해 중단되었습니다.")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ 오류 발생: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
