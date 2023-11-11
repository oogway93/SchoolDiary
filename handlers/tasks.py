# import asyncio
#
# import schedule
#
# from handlers.handlers import sending, noon_print
#
#
# async def scheduler():
#     schedule.every().day.at("13:05").do(noon_print)
#     while True:
#         await schedule.run_pending()
#         await asyncio.sleep(0.1)
