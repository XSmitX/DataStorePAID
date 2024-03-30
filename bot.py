from pyrogram import Client, filters
import pymongo
import os
from datetime import datetime
import pytz
from fpdf import FPDF
import asyncio 
from config import ADMIN
bot = Client("databt",
             bot_token="7196294857:AAEBOmgpBcppLN2IEpsTyBcUI9ef7zPjDpc",
             api_id=17249531,
             api_hash="b67965c13be2164d8a2bb6d035a1076a")
client = pymongo.MongoClient("mongodb+srv://smit:smit@cluster0.pjccvjk.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client["telegram_bot2"]
idstoring = db["ids"]

indian_timezone = pytz.timezone("Asia/Kolkata")


admins = [int(admin_id) for admin_id in ADMIN.split(',')]


@bot.on_message(filters.command("start"))
async def start(bot,message):
    if message.from_user.id not in admins:
        await bot.send_message(message.chat.id, "<b>You are not an admin of this bot.</b>")
        return
    await bot.send_photo(message.chat.id, "https://postimg.cc/215FBSHZ",f'''<b>Dear {message.from_user.first_name},

Welcome to MV UTR Checker Here You can Save your UTR Details

Press /help to know more information.                         
Note : Only admins can access this bot currently!</b>''')

@bot.on_message(filters.command("help"))
async def help_command(bot, message):
    if message.from_user.id not in admins:
        await bot.send_message(message.chat.id, "<b>You are not an admin of this bot.</b>")
        return
    help_message = """
<b>How to Use MV UTR Checker Bot:</b>

1. <b>Start the Bot:</b>
    <code>- Click on the "Start" button or send /start to initiate the bot.</code>
    
2. <b>Save UTR Details:</b>
    <code>- To save UTR details, send the UTR ID followed by the amount on separate lines in the format:</code>
        ```
        UTR ID
        Amount
        ```
    <code>- Make sure to enter the UTR ID (between 10 to 30 characters) and the amount correctly.</code>
    
3. <b>View All Data:</b>
    <code>- To view all saved UTR details, send /show.</code>
    
4. <b>Generate PDF for a Specific Date:</b>
    <code>- To generate a PDF containing UTR details for a specific date, send /data followed by the date in the format dd mm yyyy (e.g., /data 29 03 2024).</code>

<b>Notes:</b>
<code>- Only admins can access this bot.
- Make sure to provide correct details while saving UTR.
- Use the provided commands to interact with the bot.</code>

"""
    await message.reply_text(help_message)
def generate_pdf_all():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    page_width = 210  # Width of the PDF page in millimeters (A4 size)
    available_width = page_width - (pdf.l_margin + pdf.r_margin)  # Calculate available width
    
    # Calculate column widths
    no_width = available_width * 0.08  # Adjusted for the "No." column
    id_width = available_width * 0.3  # 25% of available width
    price_width = available_width * 0.25  # 20% of available width
    date_width = available_width * 0.18  # 25% of available width
    time_width = available_width * 0.2  # 30% of available width
    
    # Add headers
    pdf.set_font("Arial", style="B", size=12)
    pdf.cell(no_width, 10, "UTR", border=1)
    pdf.cell(id_width, 10, "ID", border=1)
    pdf.cell(price_width, 10, "Amount", border=1)
    pdf.cell(date_width, 10, "Date", border=1)
    pdf.cell(time_width, 10, "Time", border=1)
    pdf.ln()

    # Set font back to regular
    pdf.set_font("Arial", size=12)

    # Query all documents
    documents = idstoring.find()

    # Counter for the "No." column
    row_number = 1

    for doc in documents:
        pdf.cell(no_width, 10, str(row_number), border=1)  # Add row number
        pdf.cell(id_width, 10, str(doc['id']), border=1)
        pdf.cell(price_width, 10, '{:,.0f}'.format(doc['amount'])+"/-", border=1)
        pdf.cell(date_width, 10, str(doc['date']).replace(" ","/"), border=1)
        pdf.cell(time_width, 10, str(doc['time']), border=1)
        pdf.ln()

        # Increment row number
        row_number += 1

    pdf.output(f"all_data.pdf")

def generate_pdf(date):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    page_width = 210  # Width of the PDF page in millimeters (A4 size)
    available_width = page_width - (pdf.l_margin + pdf.r_margin)  # Calculate available width
    
    # Calculate column widths
    no_width = available_width * 0.08  # Adjusted for the "No." column
    id_width = available_width * 0.3  # 25% of available width
    price_width = available_width * 0.25  # 20% of available width
    date_width = available_width * 0.18  # 25% of available width
    time_width = available_width * 0.2  # 30% of available width
    
    # Add headers
    pdf.set_font("Arial", style="B", size=12)
    pdf.cell(no_width, 10, "UTR", border=1)
    pdf.cell(id_width, 10, "ID", border=1)
    pdf.cell(price_width, 10, "Amount", border=1)
    pdf.cell(date_width, 10, "Date", border=1)
    pdf.cell(time_width, 10, "Time", border=1)
    pdf.ln()

    # Set font back to regular
    pdf.set_font("Arial", size=12)

    query = {"date": date}
    documents = idstoring.find(query)

    # Counter for the "No." column
    row_number = 1
    #f"{str(doc['amount'])}/-"
    #'{:,.0f}'.format(doc['amount'])+"/-"
    for doc in documents:
        pdf.cell(no_width, 10, str(row_number), border=1)  # Add row number
        pdf.cell(id_width, 10, str(doc['id']), border=1)
        pdf.cell(price_width, 10, '{:,.0f}'.format(doc['amount'])+"/-", border=1)
        pdf.cell(date_width, 10, str(doc['date']).replace(" ","/"), border=1)
        pdf.cell(time_width, 10, str(doc['time']), border=1)
        pdf.ln()

        # Increment row number
        row_number += 1

    pdf.output(f"data_{date}.pdf")

@bot.on_message(filters.command("data"))
async def data_command(client, message):
    if message.from_user.id not in admins:
        await bot.send_message(message.chat.id, "<b>You are not an admin of this bot.</b>")
        return
    _,date = message.text.split("/data ") # Extract date from command
    print(date)
    generate_pdf(date)
    await message.reply_document(document=f"data_{date}.pdf")
    os.remove(f"data_{date}.pdf")

@bot.on_message(filters.command('show'))
async def show_command(bot, message):
    if message.from_user.id not in admins:
        await bot.send_message(message.chat.id, "<b>You are not an admin of this bot.</b>")
        return
    generate_pdf_all()
    await message.reply_document(document="all_data.pdf")
    os.remove(f"all_data.pdf")
@bot.on_message(filters.text & filters.private)
async def datastore(bpt,message):
    try:
        if message.from_user.id not in admins:
            await bot.send_message(message.chat.id, "<b>You are not an admin of this bot.</b>")
            return
        data,price = message.text.split('\n')
        if len(data) < 10 or len(data) > 30:
            await bot.send_message(message.chat.id, "<b>Entered UTR is invalid.</b>")
            return
        amount = int(price)
  
        text = message.text
        lines = text.splitlines()
        current_time = datetime.now(indian_timezone).strftime("%I:%M:%S %p")
        #current_time = datetime.now(indian_timezone).strftime("%H:%M:%S")
        current_date = datetime.now(indian_timezone).strftime("%d %m %Y")

        existing_entry = idstoring.find_one({"id": data })
        if existing_entry:
            await bot.send_photo(message.chat.id, "https://postimg.cc/Yjfs6jxn",'''<b>Error ‼️⚠️

Your Provided Details hasn’t been saved in MV UTR Database Because This ID is Already Exists in Our System !

Please Check The UTR ID Correctly Then Resend It. ✅

Regards 
MV UTR Checker</b>''')
        else:

            entry = {
                "id": data,
                "amount" : amount,
                "time": current_time,
                "date": current_date
            }
            idstoring.insert_one(entry)

            
            await bot.send_photo(message.chat.id,"https://postimg.cc/jnXPLpPc",f'''<b>Your Provided Details has been successfully Saved in MV UTR Database ! 

UTR 🆔 : {data}
Amount 💸 : {amount}/-
Date 📌 : {current_date} 
Time 🕰️ : {current_time}

Thankyou 
MV UTR Checker
</b>''')
            # Send the image to the user
    except:
        incorrect = await bot.send_message(message.chat.id , "<i><b>Incorrect Details \nPlease enter correct details.</b></i>")
        await asyncio.sleep(5)
        await message.delete()
        await incorrect.delete()


    

bot.run()
