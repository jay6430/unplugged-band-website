# Event media manifest. SRC paths are read-only; nothing is ever written into media/.
SRC = "media/Portfolio"

EVENTS = [
 dict(id="saputara", src_dirs=["Saputara monsoon Fest/2026", "Saputara monsoon Fest/2025"],
   photos=[
     ("Saputara monsoon Fest/2026/0P9A4946.JPG",              "Full band on the Monsoon Festival main stage"),
     ("Saputara monsoon Fest/2026/live-performance-flags.jpg","Independence Day set, tricolour flying"),
     ("Saputara monsoon Fest/2026/06-lead-vocals-guitar.jpg", "Rajat Lad on lead vocals and guitar"),
     ("Saputara monsoon Fest/2026/05-stage-production-wide.jpg","Government of Gujarat stage production"),
     ("Saputara monsoon Fest/2025/2025_08_14_19_32_IMG_1529.JPG","On stage under the Saputara Monsoon Festival banner"),
     ("Saputara monsoon Fest/2025/2025_08_14_19_24_IMG_1524.JPG","Kunjan Patel behind the kit, band backdrop up"),
     ("Saputara monsoon Fest/2025/2025_08_14_20_19_IMG_1561.JPG","The view from the drum riser"),
     ("Saputara monsoon Fest/2025/2025_08_14_20_41_IMG_1596.JPG","Full house at the festival pavilion"),
     ("Saputara monsoon Fest/2025/2025_08_14_20_51_IMG_1605.JPG","Dev Patel on keys beside the tricolour"),
     ("Saputara monsoon Fest/2025/2025_08_14_20_20_IMG_1564.JPG","Jay Patel on bass"),
     ("Saputara monsoon Fest/2025/2025_08_14_18_54_IMG_1508.JPG","The huddle before walking on"),
   ],
   loops=[
     ("Saputara monsoon Fest/2025/illahi.mp4",       80, "Illahi"),
     ("Saputara monsoon Fest/2025/teri deewani.mp4",100, "Teri Deewani"),
     ("Saputara monsoon Fest/2026/1 main reel.MOV",   4, "2026 highlights"),
   ]),

 dict(id="hillside", src_dirs=["Hillside sunset concert (Dang)"],
   photos=[
     ("Hillside sunset concert (Dang)/DSCF3584.JPG",       "Sunset over the Dang hills, mid-set"),
     ("Hillside sunset concert (Dang)/DSCF3563.JPG",       "Blue hour, the crowd still standing"),
     ("Hillside sunset concert (Dang)/Ride_220626_043.jpg","Golden hour, hills behind the stage"),
     ("Hillside sunset concert (Dang)/Ride_220626_044.JPG","No barricade, no stage, just a hillside"),
     ("Hillside sunset concert (Dang)/DSCF3525.JPG",       "Riders and locals gathering as we set up"),
     ("Hillside sunset concert (Dang)/Ride_220626_056.jpg","Phone torches instead of stage lights"),
     ("Hillside sunset concert (Dang)/DSC05482.JPG",       "The crowd after dark"),
     ("Hillside sunset concert (Dang)/DSC05469.JPG",       "Our view from the stage"),
     ("Hillside sunset concert (Dang)/Ride_220626_053.jpg","Guitar, torchlight and hills"),
   ],
   loops=[
     ("Hillside sunset concert (Dang)/IMG_9703.MOV", 60, "Hillside set"),
     ("Hillside sunset concert (Dang)/IMG_9702.MOV", 20, "Sunset session"),
   ]),

 dict(id="cafes", src_dirs=["cafes and clubs"], photos=[],
   loops=[
     ("cafes and clubs/Antosocial club 1.MOV",      12, "AntiSocial, Lower Parel"),
     ("cafes and clubs/Antosocial club 2.MOV",      60, "AntiSocial, Mumbai"),
     ("cafes and clubs/Antosocial club 3.MOV",      30, "AntiSocial, live"),
     ("cafes and clubs/Foodaholic Cafe Valsad.MOV", 60, "Foodaholic Cafe, Valsad"),
   ]),

 dict(id="corporate", src_dirs=["corporate"],
   photos=[
     ("corporate/Rajat lad singer.jpg",     "Rajat Lad on vocals"),
     ("corporate/Kunjan Patel drums.jpg",   "Kunjan Patel on drums"),
     ("corporate/Dev patel keys.jpg",       "Dev Patel on keys"),
     ("corporate/jay patel bass guitar.jpg","Jay Patel on bass"),
   ],
   loops=[
     ("corporate/Corporate 1.1.mp4", 60, "Corporate night"),
     ("corporate/Corporate 2.1.mp4",120, "Annual day set"),
     ("corporate/Corporate 2.2.mp4", 80, "Company celebration"),
   ]),

 dict(id="diwali", src_dirs=["Diwali newyear and open performances"], photos=[],
   loops=[
     ("Diwali newyear and open performances/Diwali new year performance.mp4", 20, "Diwali open concert"),
     ("Diwali newyear and open performances/Open live gig tithal.mp4",        10, "Open gig, Tithal"),
     ("Diwali newyear and open performances/Tithal audience feedback.mp4",    20, "Tithal, the crowd"),
   ]),

 dict(id="wedding", src_dirs=["wedding reception"], photos=[],
   loops=[
     ("wedding reception/saaiyan.mp4",                 40, "Saaiyan, sangeet night"),
     ("wedding reception/love thoda.mp4",              40, "Reception set"),
     ("wedding reception/video_20251124_214238.mp4",  120, "Wedding night"),
     ("wedding reception/video_20251124_232043.mp4",   60, "Late into the reception"),
   ]),
]
