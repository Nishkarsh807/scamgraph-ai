"""
ScamGraph AI - Dataset Generator & Preprocessor
Generates authentic Indian English & Hinglish scam and benign datasets covering all required fraud categories.
Produces stratified splits: 70% train, 15% validation, 15% test.
"""

import os
import json
import random
import pandas as pd
from sklearn.model_selection import train_test_split

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
RAW_DIR = os.path.join(DATA_DIR, "raw")
PROCESSED_DIR = os.path.join(DATA_DIR, "processed")

os.makedirs(RAW_DIR, exist_ok=True)
os.makedirs(PROCESSED_DIR, exist_ok=True)

# Authentic scam samples across 12 specific fraud categories
SCAM_SAMPLES = [
    # KYC
    ("Dear SBI Customer, your YONO account has been suspended due to pending KYC. Click http://sbi-kyc-update.xyz to verify immediately or account will be blocked permanently.", "scam", "kyc", "english"),
    ("URGENT: Your HDFC Bank account KYC expired today. Submit PAN & Aadhaar details at http://hdfc-netverify.live to avoid account freeze within 24 hours.", "scam", "kyc", "english"),
    ("Aapka SBI account block ho jayega, KYC update karein turant link par click karke: http://sbi-kyc-portal.top/login", "scam", "kyc", "hinglish"),
    ("ICICI Alert: Your NetBanking service will be deactivated. Update Pan Card and Aadhaar verification now at https://icici-kyc-renew.site", "scam", "kyc", "english"),
    ("Dear customer, your Paytm wallet KYC is incomplete. Your wallet balance ₹4,500 will be frozen. Call helpline 9823419821 or visit http://paytm-wallet-kyc.in", "scam", "kyc", "english"),
    ("Airtel Payments Bank: Your account has been temporarily disabled. Upload KYC documents via http://airtel-bank-verify.info to restore access.", "scam", "kyc", "english"),
    ("Priye grahak, aapka bank khata aadhar se link nahi hai. 12 ghante ke andar http://kyc-aadhaar-link.com pe jake update karein varna khata band ho jayega.", "scam", "kyc", "hinglish"),
    ("Axis Bank notification: Important update. Your account KYC documents have been rejected. Click http://axis-document-renew.vip to submit PAN card.", "scam", "kyc", "english"),
    ("Kotak 811 account notice: Your KYC verification has lapsed. Download our verification APK from http://kotak-support-app.apk and complete biometric check.", "scam", "kyc", "english"),
    ("Your PNB account KYC status is EXPIRED. Click http://pnb-online-kyc.org to avoid stoppage of ATM and UPI transactions.", "scam", "kyc", "english"),
    ("Bank alert: Dear user, KYC mandatory verification pending. Link: http://bank-kyc-service.cc. Failure will attract penalty of ₹500.", "scam", "kyc", "english"),
    ("Aapka bank KYC expire ho gaya hai. Abhi update kare http://sbi-quick-kyc.biz nahi to kal se UPI kaam nahi karega.", "scam", "kyc", "hinglish"),

    # UPI
    ("You have received a cashback refund of ₹2,500 from PhonePe. To receive the money directly into your bank, click http://phonepe-refund-claim.in and enter your UPI PIN.", "scam", "upi", "english"),
    ("Google Pay: You have won a golden scratch card worth ₹4,999! Accept UPI collect request and enter secret PIN to claim instantly into your bank account.", "scam", "upi", "english"),
    ("Bhai maine aapko ₹5,000 galti se bhej diye hain. Please return kar do. Is collect request ko approve karke apna UPI PIN daal do.", "scam", "upi", "hinglish"),
    ("Paytm Refund: Your failed transaction of ₹1,850 has been reversed. Tap link to approve UPI mandate and credit amount: http://paytm-reversal.live", "scam", "upi", "english"),
    ("Amazon Pay reward: You have a pending cashback of ₹3,000. Open PhonePe/GPay and enter your UPI PIN to receive money in your account.", "scam", "upi", "english"),
    ("OLX Buyer: I am in the Indian Army. I want to buy your furniture. I have sent UPI QR code. Scan QR code and enter UPI PIN to receive ₹15,000 payment.", "scam", "upi", "english"),
    ("Paise receive karne ke liye Google Pay par QR scan karein aur 6-digit UPI PIN enter karein. Turant account mein credit hoga.", "scam", "upi", "hinglish"),
    ("BHIM UPI alert: Suspicious activity observed. Validate your UPI ID and PIN at http://bhim-upi-security.me to prevent unauthorized debit.", "scam", "upi", "english"),
    ("Your Cred cashback of ₹1,200 is ready. Enter your UPI ID and PIN at http://cred-rewards-claim.xyz to withdraw.", "scam", "upi", "english"),
    ("Payment of ₹8,000 initiated by Rohit Kumar. Click to accept and authenticate via UPI PIN: http://upi-collect-pay.link", "scam", "upi", "english"),

    # OTP
    ("SBI Customer Support: We detected an unauthorized transaction of ₹49,999 on your card. To block this payment, please tell the 6-digit OTP sent to your phone immediately.", "scam", "otp", "english"),
    ("Dear user, courier delivery attempt failed for parcel #DEL8921. Share OTP sent to your mobile with delivery executive to reschedule.", "scam", "otp", "english"),
    ("Aapke credit card se international transaction attempt hua hai. Ise cancel karne ke liye abhi aaya hua OTP hamare executive ko batayein.", "scam", "otp", "hinglish"),
    ("WhatsApp security alert: Someone is trying to register WhatsApp with your number. Forward the 6-digit code received via SMS to verify identity.", "scam", "otp", "english"),
    ("Bank Manager speaking: Your debit card is being renewed. Please provide the OTP received on SMS to activate your new chip card.", "scam", "otp", "english"),
    ("Aadhaar authentication failed. An OTP has been dispatched to your mobile. Send this code to 9123849102 to prevent Aadhaar cancellation.", "scam", "otp", "english"),
    ("NetBanking password reset request generated. If you did not request this, share the security token OTP with support agent at +91-9876543210 to abort.", "scam", "otp", "english"),
    ("Sir aapka electricity meter update ho raha hai. Abhi jo OTP aaya hai wo share karein taaki power supply uninterrupted rahe.", "scam", "otp", "hinglish"),
    ("Congratulations! You won iPhone 15 in lottery. Share the verification OTP to confirm your delivery address.", "scam", "otp", "english"),

    # Phishing
    ("Income Tax Department: Refund of INR 26,490 has been approved for your PAN. Click http://incometax-refund-gov.link to verify your bank account details.", "scam", "phishing", "english"),
    ("Urgent: Your Netflix subscription failed. Update billing details at http://netflix-payment-portal.info within 12 hours to avoid account termination.", "scam", "phishing", "english"),
    ("India Post: Your package #IN98129 cannot be delivered due to incomplete street address. Update details and pay ₹5 re-delivery fee at http://indiapost-parcel-tracking.vip", "scam", "phishing", "english"),
    ("Aapka income tax refund pending hai ₹18,750. Apne bank details yaha submit karein: http://it-refund-portal.org", "scam", "phishing", "hinglish"),
    ("Facebook Security: Your page is scheduled for deletion due to copyright infringement. Submit appeal at http://meta-copyright-appeal.site", "scam", "phishing", "english"),
    ("Apple ID Locked: Your iCloud account has been locked for security reasons. Verify your Apple ID and password at http://icloud-support-verify.cc", "scam", "phishing", "english"),
    ("EPFO Alert: Claim of ₹42,000 processed. Login to http://epfo-claim-status.xyz with UAN and password to verify bank details.", "scam", "phishing", "english"),
    ("Speed Post: Consignment arrived at hub. Pay customs clearance ₹25 at http://postal-clearance-online.in to dispatch.", "scam", "phishing", "english"),

    # Fake Bank Support
    ("Dear HDFC customer, for any transaction dispute or refund call our 24x7 toll free customer care at +91-8921829102 immediately.", "scam", "banking", "english"),
    ("SBI Alert: Your NetBanking user ID has been locked after 3 invalid attempts. Call official helpline 9182391029 or install QuickSupport app to unlock.", "scam", "banking", "english"),
    ("Namaste, main Bank of Baroda head office se bol raha hoon. Aapke account mein technical issue hai, AnyDesk app download karke 9-digit code batayein.", "scam", "banking", "hinglish"),
    ("Canara Bank customer notice: Your reward points worth ₹7,850 are expiring tonight. Redeem points into cash by calling support executive at +91-7654321098.", "scam", "banking", "english"),
    ("Bank Support: Install SBI Quick Support application from http://sbi-support-tool.apk to resolve pending debit issue.", "scam", "banking", "english"),
    ("ICICI bank credit card executive: We are waiving off your annual fees. Please provide card CVV and expiry date for system waiver.", "scam", "banking", "english"),
    ("Aapke account se bina permission ke ₹12,000 kat gaye hain? Turant hamare customer support number 9311029481 par call karein refund lene ke liye.", "scam", "banking", "hinglish"),

    # Job Scam
    ("Earn ₹2,000 - ₹5,000 daily working from home! Simple YouTube video liking and Google reviews task. Telegram @hr_priya_tasks to start immediately.", "scam", "job", "english"),
    ("Part time online job opportunity: Earn ₹1,500 per hour by evaluating Amazon products. No experience needed. WhatsApp +91-9876501234 for details.", "scam", "job", "english"),
    ("Ghar baithe kaam karein aur kamayein ₹30,000 mahina. Data entry aur typing work. Registration fee sirf ₹499. Sampark karein Telegram pe.", "scam", "job", "hinglish"),
    ("Congratulations! You have been selected for Data Analyst position at Google India. Salary 12 LPA. Pay document processing fee ₹2,500 to receive offer letter.", "scam", "job", "english"),
    ("Work from home task job: Like 3 Instagram reels and get ₹150 instantly into UPI. Deposit ₹1,000 VIP trading task to withdraw ₹5,000.", "scam", "job", "english"),
    ("Airline Ground Staff Vacancy: Indigo hiring 250 candidates. Direct joining without interview. Security deposit ₹3,500 refundable. Apply now.", "scam", "job", "english"),
    ("Aapko part time job ke liye select kiya gaya hai. Har din 2 ghante mobile pe task karein aur ₹2,000 kamayein. WhatsApp karein link par click karke.", "scam", "job", "hinglish"),

    # Loan Scam
    ("Instant Personal Loan Approved: ₹5,00,000 approved at 2% annual interest without CIBIL score. Pay processing fee of ₹1,999 to disburse funds within 10 mins.", "scam", "loan", "english"),
    ("Dhani Loan: Your loan sanction letter of ₹2,50,000 is ready. Download app from http://dhaniloan-quick-apk.xyz and pay insurance charge ₹999 to get loan.", "scam", "loan", "english"),
    ("Aapka ₹1,00,000 ka pre-approved loan pass ho gaya hai bina kisi paper ke. 5 minute mein paisa account mein paane ke liye processing fee ₹1,500 jama karein.", "scam", "loan", "hinglish"),
    ("Bajaj Finance Pre-Approved Loan: ₹3,00,000 at 0% EMI. Pay GST verification charges ₹2,450 to release payment to your account.", "scam", "loan", "english"),
    ("Urgent Loan Notification: Emergency loan approved for your Aadhaar card. Transfer stamp duty fee ₹850 via UPI to activate disbursement.", "scam", "loan", "english"),
    ("7 Days Instant Loan App: Get ₹50,000 immediately without salary slip. Upload your contact list and PAN card to verify.", "scam", "loan", "english"),

    # Lottery / Cashback
    ("Kaun Banega Crorepati (KBC) Official Announcement: Your WhatsApp mobile number has won ₹25,00,000 in lucky draw! Contact KBC Manager Rana Pratap on WhatsApp +91-7890123456 to claim.", "scam", "lottery", "english"),
    ("Badhai ho! Aapke mobile number ko Jio 5G lucky draw mein ₹15,00,000 ka inaam mila hai. Lottery claim karne ke liye registration fee ₹2,500 transfer karein.", "scam", "lottery", "hinglish"),
    ("Congratulations! You are the grand winner of ₹10,00,000 in Car Lottery. Transfer government GST amount ₹12,000 to release prize money.", "scam", "lottery", "english"),
    ("Paytm Mega Offer: You have won a Tata Nexon SUV or cash prize ₹7,50,000. Send processing fee ₹3,200 via UPI to dispatch vehicle.", "scam", "lottery", "english"),
    ("Aapka number KBC lottery winner list mein aa gaya hai. YouTube video dekhein aur manager ko WhatsApp par lottery number KBC-092 bhejein.", "scam", "lottery", "hinglish"),

    # Electricity Bill Scam
    ("Dear Consumer, your electricity power supply will be disconnected tonight at 9:30 PM from the power sub-station because your previous month bill was not updated. Immediately contact Electricity Officer Sharma at 9876543210.", "scam", "electricity", "english"),
    ("Mahavitaran Alert: Power will be disconnected at 10 PM tonight due to unpaid bill of ₹840. Call our power office helpline 8912304910 to avoid disconnection.", "scam", "electricity", "english"),
    ("Priye upbhokta, aapki bijli aaj raat 9:30 baje kaat di jayegi kyunki pichle mahine ka bill jama nahi hua. Turant bijli adhikari se sampark karein 9821039102 par.", "scam", "electricity", "hinglish"),
    ("BSES Rajdhani notice: Urgent power disconnection order issued for meter #29104. Pay ₹10 bill verification fee via link http://bses-bill-portal.in to clear dues.", "scam", "electricity", "english"),
    ("UPPCL Bijli Vibhag: Aaj sham tak bill jama na karne par transformer se connection disconnect kar diya jayega. Call SDO officer at 9123984012.", "scam", "electricity", "hinglish"),
    ("Electricity Board: Your meter software update is pending. Electricity connection will be cut in 2 hours. Call 9812903481 to install patch.", "scam", "electricity", "english"),

    # Investment Scam
    ("Guaranteed Stock Market Tips: Earn 500% profit in 7 days! Join our VIP Telegram channel for insider crypto and forex trade calls. Deposit ₹10,000 to get ₹50,000 return.", "scam", "investment", "english"),
    ("Goldman Sachs Quantitative Trading Platform: Automated AI bot earns 15% daily return. Register at http://gs-crypto-invest.xyz and deposit USDT to start.", "scam", "investment", "english"),
    ("Ghar baithe crypto trading se har hafte ₹50,000 kamayein. Initial investment sirf ₹5,000. 100% safe aur RBI registered platform.", "scam", "investment", "hinglish"),
    ("Institutional High-Yield Arbitrage Fund: Minimum deposit ₹25,000. Daily compounding payout credited directly to bank account. Limited slots.", "scam", "investment", "english"),
    ("IPO Allotment Guaranteed: We have special institutional quota for Tata Technologies IPO. Transfer application money ₹15,000 to our trustee bank account.", "scam", "investment", "english"),

    # Digital Arrest Scam
    ("This is Inspector Rajesh Kumar from Mumbai Cyber Crime Branch. A FedEx parcel sent in your name containing 5 passports, 160 grams MDMA drugs and fake currency has been seized at airport customs. You are under digital arrest. Stay on video call and do not contact anyone.", "scam", "digital_arrest", "english"),
    ("CBI Headquarters New Delhi: An arrest warrant has been issued against your Aadhaar card for laundering ₹3.8 Crores in the Naresh Goyal bank fraud case. Transfer all funds into RBI safety verification escrow account immediately to prove your innocence.", "scam", "digital_arrest", "english"),
    ("TRAI / Telecom Department Alert: All SIM cards registered on your Aadhaar will be disconnected within 2 hours due to illegal harassment complaints. Connect to Supreme Court digital hearing via Skype now.", "scam", "digital_arrest", "english"),
    ("Delhi Police Crime Branch: You have received a summons regarding child pornography and extortion charges. A court warrant is issued. Report on video interrogation immediately or police team will arrive at your address.", "scam", "digital_arrest", "english"),
    ("Customs Officer at Mumbai Airport: Aapke naam se ek parcel pakda gaya hai jisme illegal items hain. Bachne ke liye abhi police verification deposit jama karein.", "scam", "digital_arrest", "hinglish"),

    # Impersonation
    ("Hey dad, I lost my phone and my wallet while traveling in Mumbai. I am using my friend's phone. Please send ₹12,000 urgently on this UPI ID: friend.emergency@upi. Urgent emergency please don't call.", "scam", "impersonation", "english"),
    ("Hello, I am Amit, CEO of your company. I am currently in a confidential client meeting and cannot take calls. Please buy 5 Apple App Store Gift cards worth ₹10,000 each and email the voucher codes to me right away.", "scam", "impersonation", "english"),
    ("Bhai emergency ho gayi hai, accident mein hospital mein admit hoon. Turant ₹8,000 is UPI pe send kar: rahul.care99@okicici. Sham ko wapas kar dunga.", "scam", "impersonation", "hinglish"),
    ("Indian Army Subedar posting transfer: Selling my Royal Enfield Bullet 350cc (2022 model) for only ₹60,000 as I got transfer to Leh. Pay gate pass fee ₹5,000 for army cantonment vehicle release.", "scam", "impersonation", "english"),
    ("Dear employee, HR department notice: Your appraisal bonus of ₹35,000 requires salary bank verification. Open link http://company-hr-portal.me/verify to confirm.", "scam", "impersonation", "english"),
]

# Authentic Benign samples
BENIGN_SAMPLES = [
    ("Your SBI account XX3829 debited by INR 350.00 on 08-Oct-26 at SWIGGY. Avail Bal: INR 18,450.20. If not done by you, SMS BLOCK to 567676.", "benign", "banking", "english"),
    ("682910 is your OTP for logging into HDFC NetBanking. Valid for 3 minutes. Do not share this OTP with anyone, including bank staff.", "benign", "banking", "english"),
    ("Paid ₹450 to Blue Tokai Coffee via Google Pay. UPI Transaction ID: 429182049102. Bank Reference No: 9182039182.", "benign", "upi", "english"),
    ("Dear Customer, electricity bill for CA No. 102938491 is ₹1,850. Due date is 18-Oct-2026. Pay securely via our official website www.bsesdelhi.com.", "benign", "electricity", "english"),
    ("Your Amazon order #402-9182391-10293 has been dispatched and will arrive tomorrow. Track package on your Amazon mobile app.", "benign", "other", "english"),
    ("Your Zomato order has been picked up by delivery partner Rahul. Estimated delivery time: 25 minutes.", "benign", "other", "english"),
    ("Bhai kal sham ko 6 baje badminton court pe milte hain. Time pe pahuch jana.", "benign", "other", "hinglish"),
    ("Can you please send me the financial report presentation slides before our sync meeting at 3 PM?", "benign", "other", "english"),
    ("Dear Taxpayer, your Income Tax Return for AY 2025-26 has been successfully verified. Acknowledgment number: 981290381029.", "benign", "other", "english"),
    ("591024 is the one time password (OTP) for your Zomato order payment of ₹620. Do not disclose to anyone.", "benign", "banking", "english"),
    ("Dear Airtel subscriber, your daily 1.5 GB high-speed data limit has reached 50%. Top up anytime via Airtel Thanks App.", "benign", "other", "english"),
    ("Reminder: Doctor appointment with Dr. Mehta confirmed for tomorrow 11:30 AM at Apollo Clinic.", "benign", "other", "english"),
    ("Salary of INR 85,000.00 credited to your ICICI Bank account XX9102 on 30-Sep-2026. Available balance INR 1,12,450.00.", "benign", "banking", "english"),
    ("Your Flipkart return pickup has been scheduled for today between 10 AM and 2 PM. Delivery agent will verify product condition.", "benign", "other", "english"),
    ("Papa maine train ticket book kar li hai. 12 October ko shaam ko 7 baje pahuch jaunga.", "benign", "other", "hinglish"),
    ("Dear customer, thank you for visiting Reliance Digital. Your invoice has been emailed to your registered address.", "benign", "other", "english"),
    ("Your PhonePe recharge of ₹299 for mobile 9876543210 was successful. Operator Ref: BR91823901.", "benign", "upi", "english"),
    ("Team meeting rescheduled to Friday 11:00 AM IST. Please check your Google Calendar invitation.", "benign", "other", "english"),
    ("Your Uber ride OTP is 3910. Share this with driver Sanjay once you board the vehicle.", "benign", "other", "english"),
    ("Happy Diwali to you and your family! Wishing you joy, peace and prosperity in the coming year.", "benign", "other", "english"),
    ("Dear cardholder, your credit card statement for ending 4019 is generated. Total due ₹14,200, minimum due ₹1,200 due on 22-Oct-2026.", "benign", "banking", "english"),
    ("Congratulations on clearing the AWS Certified Solutions Architect exam! Your digital badge is ready on Credly.", "benign", "other", "english"),
    ("Bhai project code review finish kar diya hai maine GitHub pe. PR merge kar le.", "benign", "other", "hinglish"),
    ("Your IndiGo flight 6E-204 from Delhi to Bengaluru departs at 07:15 AM from Terminal 3. Web check-in open.", "benign", "other", "english"),
    ("Dear customer, your request for address update in bank records has been submitted at our branch. Reference: REQ82910.", "benign", "banking", "english"),
    ("Your Netflix monthly subscription has been renewed successfully for ₹649. Next billing date: 08-Nov-2026.", "benign", "other", "english"),
    ("Sir, I have submitted the pull request for the authentication service bugfix. Please review whenever free.", "benign", "other", "english"),
    ("Gas cylinder booking #82910 confirmed. Delivery expected within 48 hours. Cash on delivery amount: ₹830.", "benign", "other", "english"),
    ("Dear customer, maintenance activity scheduled on HDFC Bank NetBanking on Sunday from 01:00 AM to 04:00 AM.", "benign", "banking", "english"),
    ("Aapka internet broadband plan renew ho gaya hai ₹999 mein. 30 din ki validity activate ho gayi hai.", "benign", "other", "hinglish"),
    ("Thanks for paying ₹1,200 at Starbucks using your Apple Pay card. Transaction reference: SBX91029.", "benign", "banking", "english"),
    ("Your courier tracking number 4091823 is out for delivery with Delhivery. Handover OTP will be asked upon delivery.", "benign", "other", "english"),
    ("School fee payment of ₹18,500 received for Student ID #29104. Receipt generated on school portal.", "benign", "other", "english"),
    ("Hello Rahul, please find attached the revised vendor agreement for your review before Monday signature.", "benign", "other", "english"),
    ("Weather alert: Moderate to heavy rain forecast in Mumbai over the next 24 hours. Plan commutes safely.", "benign", "other", "english"),
    ("Your JioFiber bill of ₹824 has been paid via Paytm. Receipt ID: JIO91823901.", "benign", "other", "english"),
    ("Dear investor, mutual fund statement for SIP dated 05-Oct-2026 has been generated in your Groww account.", "benign", "investment", "english"),
    ("Your appointment with car servicing at Maruti Service Arena is confirmed for Saturday 10 AM.", "benign", "other", "english"),
    ("Dear customer, your loan EMI of ₹8,420 for month of October has been debited successfully.", "benign", "loan", "english"),
    ("Bhai lunch ke liye canteen chalein ya bahar se Swiggy order karna hai?", "benign", "other", "hinglish"),
    ("Your Airtel DTH account 30192849 has been recharged with ₹450 for 30 days. Channels active.", "benign", "other", "english"),
    ("Package delivered to security gate as per delivery instructions. Have a great day!", "benign", "other", "english"),
    ("Dear employee, PF passbook for the current financial year has been updated on the EPFO portal.", "benign", "other", "english"),
    ("Aapka passport renewal appointment 24 October ko Delhi RPO mein confirm hua hai.", "benign", "other", "hinglish"),
    ("Payment of ₹3,400 received via NEFT from Ramesh Kumar. Updated account balance: ₹54,300.", "benign", "banking", "english"),
]

def augment_data():
    augmented = []
    
    # Augment Scam samples
    banks = ["SBI", "HDFC", "ICICI", "Axis", "Kotak", "Punjab National Bank", "Bank of Baroda"]
    for text, label, scam_type, lang in SCAM_SAMPLES:
        augmented.append((text, label, scam_type, lang))
        # Variation with urgency
        augmented.append((f"IMPORTANT ALERT: {text} Action required within 1 hour.", label, scam_type, lang))
        # Variation with Bank swaps
        for b in ["HDFC", "ICICI", "SBI"]:
            if any(k in text for k in ["SBI", "HDFC", "ICICI"]):
                v_text = text.replace("SBI", b).replace("HDFC", b).replace("ICICI", b)
                augmented.append((v_text, label, scam_type, lang))
                break

    # Augment Benign samples to achieve balanced representation
    merchants = ["Swiggy", "Zomato", "Amazon", "Flipkart", "Blinkit", "Myntra", "Uber", "BookMyShow"]
    amounts = ["₹199", "₹350", "₹780", "₹1,250", "₹2,400", "₹5,000", "₹12,500", "₹24,000"]
    
    for text, label, scam_type, lang in BENIGN_SAMPLES:
        augmented.append((text, label, scam_type, lang))
        # Amount variation
        for amt in amounts[:3]:
            if "₹" in text or "INR" in text:
                v_benign = text.replace("₹350", amt).replace("₹450", amt).replace("₹1,850", amt).replace("₹620", amt)
                if v_benign != text:
                    augmented.append((v_benign, label, scam_type, lang))
        # Merchant variation
        for m in merchants[:2]:
            if "SWIGGY" in text or "Swiggy" in text or "Zomato" in text or "Amazon" in text:
                v_m = text.replace("SWIGGY", m.upper()).replace("Swiggy", m).replace("Zomato", m).replace("Amazon", m)
                if v_m != text:
                    augmented.append((v_m, label, scam_type, lang))

    # Add extra everyday benign communications
    extra_benign = [
        ("Good morning! Please find the notes from yesterday's retrospective meeting attached.", "benign", "other", "english"),
        ("Bhai shaam ko gym chalna hai kya? 7 baje nikalte hain.", "benign", "other", "hinglish"),
        ("Your OTP for accessing your company Slack workspace is 819203. Valid for 10 minutes.", "benign", "other", "english"),
        ("Electricity bill receipt: Payment of ₹1,420 received against CA 2091829. Thank you.", "benign", "electricity", "english"),
        ("Dear customer, your credit card rewards point balance is 4,200 points. Redeem at netbanking.hdfcbank.com", "benign", "banking", "english"),
        ("Hey, I transferred my share of ₹650 for yesterday's dinner via UPI. Please check.", "benign", "upi", "english"),
        ("Call me once you reach the metro station. I will come pick you up.", "benign", "other", "english"),
        ("Your monthly mobile postpaid bill of ₹706.82 for 9811223344 is due on 21-Oct.", "benign", "other", "english"),
        ("Your bus ticket from Delhi to Jaipur has been confirmed on Zingbus. Seat: 14A.", "benign", "other", "english"),
        ("Papa, medicines order kar di hain Tata 1mg se, kal dopahar tak deliver ho jayengi.", "benign", "other", "hinglish"),
        ("Security verification code for your GitHub account is: 938102. Expires in 15 mins.", "benign", "other", "english"),
        ("Movie tickets for Kantara (Kannada with English subtitles) booked for tomorrow 7:30 PM at PVR.", "benign", "other", "english"),
        ("Sir, client has signed the NDA document. We can proceed with the technical architecture demo.", "benign", "other", "english"),
        ("UPI transaction of ₹120 to Chai Point is completed. UPI Ref ID: 391029103910.", "benign", "upi", "english"),
        ("Your order from Blinkit is on the way. Delivery in 8 minutes. Rider: Sonu Kumar.", "benign", "other", "english"),
        ("Can we reschedule our 1:1 call to 4:30 PM? Have a production incident to review.", "benign", "other", "english"),
        ("Happy birthday! Wishing you a fantastic year filled with success, good health and happiness!", "benign", "other", "english"),
        ("Bhai metro card recharge karwa lena, station pe line bahut lambi hoti hai subah.", "benign", "other", "hinglish"),
    ]
    for text, label, scam_type, lang in extra_benign:
        augmented.append((text, label, scam_type, lang))
        # duplicate with slight variation
        augmented.append((f"Update: {text}", label, scam_type, lang))

    return augmented

def build_dataset():
    print("Building and augmenting dataset...")
    raw_data = augment_data()
    df = pd.DataFrame(raw_data, columns=["text", "label", "scam_type", "language"])
    df = df.drop_duplicates(subset=["text"]).reset_index(drop=True)

    print(f"Total Unique Samples: {len(df)}")
    print("\nLabel Distribution:")
    print(df["label"].value_counts())
    print("\nScam Category Distribution:")
    print(df["scam_type"].value_counts())
    print("\nLanguage Distribution:")
    print(df["language"].value_counts())

    # Save raw
    raw_path = os.path.join(RAW_DIR, "scam_dataset_raw.csv")
    df.to_csv(raw_path, index=False)
    print(f"Saved raw dataset: {raw_path}")

    # Stratified split based on binary label (70% train, 15% validation, 15% test)
    train_df, temp_df = train_test_split(df, test_size=0.30, random_state=42, stratify=df["label"])
    val_df, test_df = train_test_split(temp_df, test_size=0.50, random_state=42, stratify=temp_df["label"])

    train_path = os.path.join(DATA_DIR, "train.csv")
    val_path = os.path.join(DATA_DIR, "validation.csv")
    test_path = os.path.join(DATA_DIR, "test.csv")

    train_df.to_csv(train_path, index=False)
    val_df.to_csv(val_path, index=False)
    test_df.to_csv(test_path, index=False)

    print(f"\nStratified splits saved:")
    print(f"  Train:      {len(train_df)} rows ({len(train_df)/len(df)*100:.1f}%)")
    print(f"  Validation: {len(val_df)} rows ({len(val_df)/len(df)*100:.1f}%)")
    print(f"  Test:       {len(test_df)} rows ({len(test_df)/len(df)*100:.1f}%)")

    stats = {
        "total_samples": int(len(df)),
        "train_samples": int(len(train_df)),
        "val_samples": int(len(val_df)),
        "test_samples": int(len(test_df)),
        "scam_count": int((df["label"] == "scam").sum()),
        "benign_count": int((df["label"] == "benign").sum()),
        "categories": {str(k): int(v) for k, v in df["scam_type"].value_counts().items()},
        "languages": {str(k): int(v) for k, v in df["language"].value_counts().items()}
    }

    stats_file = os.path.join(PROCESSED_DIR, "dataset_stats.json")
    with open(stats_file, "w") as f:
        json.dump(stats, f, indent=2)
    print(f"Saved dataset statistics: {stats_file}")

if __name__ == "__main__":
    build_data = build_dataset()
