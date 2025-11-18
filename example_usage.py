"""
재난·안전 체크리스트 시스템 사용 예시
"""
import sys
from pathlib import Path

# src 디렉토리를 Python 경로에 추가
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from utils.config import config
from checklist.generator import ChecklistGenerator
from checklist.templates import FacilityType, CheckPhase, FocusArea


def example_1_basic():
    """예시 1: 지자체 재난안전 점검 체크리스트 (데이터 수집 없음)"""
    print("\n" + "="*70)
    print("예시 1: 지자체 재난안전 점검 체크리스트")
    print("="*70)

    generator = ChecklistGenerator(config.settings)

    result = generator.generate(
        keyword="○○시 지자체 재난안전",
        facility_type=FacilityType.GOVERNMENT.value,
        check_phase=CheckPhase.INITIAL.value,
        collect_data=False
    )

    # Markdown 출력
    generator.export_to_markdown(result)

    print("\n✅ 지자체 재난안전 체크리스트 생성 완료!")


def example_2_with_research():
    """예시 2: 건설현장 정기 점검 체크리스트 (데이터 수집 포함)"""
    print("\n" + "="*70)
    print("예시 2: 건설현장 정기 점검 체크리스트 (데이터 수집 포함)")
    print("="*70)

    generator = ChecklistGenerator(config.settings)

    result = generator.generate(
        keyword="△△ 건설현장",
        facility_type=FacilityType.CONSTRUCTION.value,
        check_phase=CheckPhase.REGULAR.value,
        focus_area=FocusArea.SAFETY.value,
        collect_data=True  # 데이터 수집 실행
    )

    # Markdown과 JSON 모두 출력
    generator.export_to_markdown(result)
    generator.export_to_json(result)

    print("\n✅ 건설현장 정기 점검 체크리스트 생성 완료!")


def example_3_emergency_response():
    """예시 3: 의료시설 재난 대응 체크리스트"""
    print("\n" + "="*70)
    print("예시 3: 의료시설 재난 대응 체크리스트")
    print("="*70)

    generator = ChecklistGenerator(config.settings)

    result = generator.generate(
        keyword="◇◇ 의료시설",
        facility_type=FacilityType.MEDICAL.value,
        check_phase=CheckPhase.DISASTER.value,
        focus_area=FocusArea.RESPONSE.value,
        collect_data=True
    )

    generator.export_to_markdown(result)

    print("\n✅ 의료시설 재난 대응 체크리스트 생성 완료!")


def example_4_legal_compliance():
    """예시 4: 제조사업장 연간 종합 점검 (법규 중심)"""
    print("\n" + "="*70)
    print("예시 4: 제조사업장 연간 종합 점검 (법규 중심)")
    print("="*70)

    generator = ChecklistGenerator(config.settings)

    result = generator.generate(
        keyword="□□ 제조사업장",
        facility_type=FacilityType.MANUFACTURING.value,
        check_phase=CheckPhase.ANNUAL.value,
        focus_area=FocusArea.COMPLIANCE.value,
        collect_data=True
    )

    generator.export_to_markdown(result)

    # 리서치 요약 출력
    summary = result['research_summary']
    print(f"\n📊 리서치 요약:")
    print(f"  - 웹 자료: {summary['web_sources']}건")
    print(f"  - 논문: {summary['papers']}건")
    print(f"  - 기술 프로젝트: {summary['tech_projects']}건")
    print(f"  - API: {summary['apis']}건")

    print("\n✅ 제조사업장 연간 종합 점검 체크리스트 생성 완료!")


def main():
    """메인 함수"""
    print("\n" + "="*70)
    print("  재난·안전 체크리스트 시스템 - 사용 예시")
    print("="*70)

    print("\n실행할 예시를 선택하세요:")
    print("1. 지자체 재난안전 점검 (빠름)")
    print("2. 건설현장 정기 점검 (데이터 수집 포함)")
    print("3. 의료시설 재난 대응")
    print("4. 제조사업장 연간 종합 점검")
    print("0. 종료")

    choice = input("\n선택 (1-4): ").strip()

    if choice == '1':
        example_1_basic()
    elif choice == '2':
        example_2_with_research()
    elif choice == '3':
        example_3_emergency_response()
    elif choice == '4':
        example_4_legal_compliance()
    elif choice == '0':
        print("종료합니다.")
        return
    else:
        print("잘못된 선택입니다.")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n중단되었습니다.")
    except Exception as e:
        print(f"\n오류 발생: {e}")
        import traceback
        traceback.print_exc()
