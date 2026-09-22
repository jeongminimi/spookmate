import psycopg2

# 2단계에서 복사한 주소를 넣고, 비밀번호(tkfkdgo91!SPDB)를 정확히 입력합니다.
DB_URL = "postgresql://postgres.aywtiggvataezyxeuexe:tkfkdgo91!SPDB@aws-0-ap-south-1.pooler.supabase.com:6543/postgres"

print("🔄 수파베이스 연결 테스트 중...")
try:
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    cur.execute("SELECT count(*) FROM yokai_compendium;")
    total = cur.fetchone()[0]
    print(f"🎉 [성공] 수파베이스와 정상 연결되었습니다! (요괴 도감 수: {total}개)")
    cur.close()
    conn.close()
except Exception as e:
    print(f"❌ [연결 실패] 에러 내용:\n{e}")