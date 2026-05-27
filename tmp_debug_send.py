import asyncio
from services.resend_service import init_resend_service_from_env

svc = init_resend_service_from_env()

async def main():
    res = await svc.send_email(subject='Debug Test', recipient='ceo@analyticsavenue.in', html='<p>hello</p>')
    print(res)

if __name__ == '__main__':
    asyncio.run(main())
