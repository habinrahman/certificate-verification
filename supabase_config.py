import os
from supabase import create_client, Client
from typing import Optional

# Set environment variables for local dev if not set
if not os.getenv('SUPABASE_URL'):
    os.environ['SUPABASE_URL'] = 'https://wyszrjhxucxblyvhrktn.supabase.co'
if not os.getenv('SUPABASE_KEY'):
    os.environ['SUPABASE_KEY'] = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...'

SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')

supabase: Optional[Client] = None
if SUPABASE_URL and SUPABASE_KEY:
    try:
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        print(f"✅ Supabase client initialized: {SUPABASE_URL}")
    except Exception as e:
        print(f"❌ Failed to initialize Supabase: {e}")
        supabase = None
else:
    print("⚠️ Missing SUPABASE_URL or SUPABASE_KEY")

# Mock fallback
MOCK_CERTIFICATES = [
    {
        "certificate_id": "CERT-001",
        "student_name": "Habin Rahman",
        "course_name": "ReactJS with Supabase",
        "completion_date": "2025-07-07",
        "certificate_url": "https://cert.microdegree.work/cert/CERT-001"
    },
    {
        "certificate_id": "HR08",
        "student_name": "HABIN",
        "course_name": "PYTHON",
        "completion_date": "2025-07-11",
        "certificate_url": "https://cert.microdegree.work/cert/HR08"
    },
    # Add others if needed
]

def get_certificate_by_id(certificate_id: str):
    """Get certificate data from Supabase by ID (with fallback to mock)"""
    global supabase

    if not supabase:
        print("⚠️ Using mock data")
        for cert in MOCK_CERTIFICATES:
            if cert['certificate_id'] == certificate_id:
                return {
                    "student_name": cert['student_name'],
                    "course": cert['course_name'],
                    "completion_date": cert['completion_date'],
                    "certificate_id": cert['certificate_id']
                }
        return None

    try:
        print(f"🔎 Fetching certificate: {certificate_id}")
        response = supabase.table('certificates').select('*').eq('certificate_id', certificate_id).execute()

        if response.data and len(response.data) > 0:
            cert = response.data[0]
            return {
                "student_name": cert['student_name'],
                "course": cert['course_name'],
                "completion_date": cert['completion_date'],
                "certificate_id": cert['certificate_id']
            }
        else:
            print(f"❌ Certificate not found: {certificate_id}")
            return None
    except Exception as e:
        print(f"⚠️ Error fetching from Supabase: {e}")
        return None


def get_all_certificates():
    """Return all certificates from Supabase (or mock)"""
    if not supabase:
        print("⚠️ Using mock data")
        return MOCK_CERTIFICATES

    try:
        response = supabase.table('certificates').select('*').execute()
        return response.data if response.data else MOCK_CERTIFICATES
    except Exception as e:
        print(f"⚠️ Error fetching all certs: {e}")
        return MOCK_CERTIFICATES


def add_sample_data():
    """Optional utility to add mock certs into DB"""
    if not supabase:
        print("❌ Supabase not initialized")
        return

    sample_data = [
        {
            "certificate_id": "SAMPLE-001",
            "student_name": "Alice",
            "course_name": "JavaScript Essentials",
            "completion_date": "2025-06-01",
            "certificate_url": "https://example.com/cert/SAMPLE-001"
        }
    ]

    try:
        for cert in sample_data:
            supabase.table('certificates').insert(cert).execute()
        print("✅ Sample data inserted")
    except Exception as e:
        print(f"❌ Failed to insert sample data: {e}")
