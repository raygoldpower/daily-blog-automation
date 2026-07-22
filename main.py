import os
import requests
import random
from datetime import datetime
import json
import re

ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
UNSPLASH_ACCESS_KEY = os.environ.get("UNSPLASH_ACCESS_KEY", "")
GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", "")
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", "")
GOOGLE_REFRESH_TOKEN = os.environ.get("GOOGLE_REFRESH_TOKEN", "")
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "")
FACEBOOK_PAGE_ID = os.environ.get("FACEBOOK_PAGE_ID", "")
FACEBOOK_ACCESS_TOKEN = os.environ.get("FACEBOOK_ACCESS_TOKEN", "")
BLOG_ID = "4393162034375416055"

SPORT_EMOJI = {
    "Soccer": "⚽", "Basketball": "🏀", "Baseball": "⚾", "General": "🏆",
    "Muscle Science": "💪", "Rehab": "🩺", "Nutrition": "🥗", "Sports Psychology": "🧠",
    "Conditioning": "🔥", "Mobility": "🤸", "Physiology": "🫀", "Physical Therapy": "🏥",
    "Biomechanics": "⚙️", "Anatomy": "🦴", "Body Balance": "⚖️", "Sports Medicine": "🩻",
}

TOPICS = [
    {"title": "Tight Ankles Are Quietly Killing Your Dribbling Speed... Nobody Tells You This", "keyword": "soccer dribbling ankle mobility", "img_keyword": "soccer dribbling", "sport": "Soccer", "series": "Dribble Mastery", "episode": 1},
    {"title": "The Acceleration Secret That Even Sprinters Can't Match in Soccer", "keyword": "soccer acceleration sprint training", "img_keyword": "soccer sprint", "sport": "Soccer", "series": "Speed Revolution", "episode": 1},
    {"title": "Hitting the Ball as Hard as You Can But Still No Goals? Check Your Hips", "keyword": "soccer shooting hip rotation power", "img_keyword": "soccer shooting", "sport": "Soccer", "series": "Shooting Mastery", "episode": 1},
    {"title": "The Hidden Endurance Training Behind Players Who Sprint in the 90th Minute", "keyword": "soccer endurance 90 minutes stamina", "img_keyword": "soccer endurance", "sport": "Soccer", "series": "Stamina Mastery", "episode": 1},
    {"title": "Players Who Blow Out Their Knees on the Field All Miss This One Drill", "keyword": "soccer knee injury prevention squat", "img_keyword": "knee injury soccer", "sport": "Soccer", "series": "Injury Prevention", "episode": 1},
    {"title": "Vertical Jump Isn't Genetic... How I Added 10cm in 3 Months", "keyword": "basketball jump plyometric training", "img_keyword": "basketball jump", "sport": "Basketball", "series": "Jump Revolution", "episode": 1},
    {"title": "Your Dribbling Isn't Stuck Because of Your Hands... It's Your Brain", "keyword": "basketball dribbling brain hand coordination", "img_keyword": "basketball dribbling", "sport": "Basketball", "series": "Handling Mastery", "episode": 1},
    {"title": "The Three-Point Secret Pro Players Don't Want You to Know", "keyword": "basketball three point wrist snap shooting", "img_keyword": "basketball shooting", "sport": "Basketball", "series": "Shooting Mastery", "episode": 1},
    {"title": "If Your Bat Speed Won't Improve, Stop Looking at Your Arms", "keyword": "baseball bat speed hip rotation", "img_keyword": "baseball batting", "sport": "Baseball", "series": "Science of Hitting", "episode": 1},
    {"title": "4 Warning Signs a Pitcher's Shoulder Is About to Break Down", "keyword": "baseball pitcher rotator cuff injury prevention", "img_keyword": "baseball pitcher shoulder", "sport": "Baseball", "series": "Science of Pitching", "episode": 1},
    {"title": "Squats Alone Won't Grow Your Quads If You're Missing This Variation", "keyword": "quadriceps squat variation muscle building", "img_keyword": "quadriceps squat", "sport": "Muscle Science", "series": "Muscle Anatomy", "episode": 1},
    {"title": "Why Only Your Hamstrings Tear During Sprints... Nobody Explains This", "keyword": "hamstring eccentric training injury prevention", "img_keyword": "hamstring exercise", "sport": "Muscle Science", "series": "Muscle Anatomy", "episode": 2},
    {"title": "Your Lower Back Pain Isn't Coming From Your Back... Meet This Muscle", "keyword": "transverse abdominis core activation back pain", "img_keyword": "core training", "sport": "Muscle Science", "series": "Core Science", "episode": 1},
    {"title": "You've Been Training Shoulders for Years and One Side Still Won't Grow", "keyword": "deltoid three heads shoulder training", "img_keyword": "shoulder deltoid workout", "sport": "Muscle Science", "series": "Upper Body Anatomy", "episode": 1},
    {"title": "People Who Keep Spraining Their Ankles All Share One Weak Muscle", "keyword": "calf muscle ankle stability injury prevention", "img_keyword": "calf muscle", "sport": "Muscle Science", "series": "Lower Body Anatomy", "episode": 1},
    {"title": "The Real Reason Your Muscles Won't Grow No Matter How Hard You Train", "keyword": "muscle protein synthesis hypertrophy", "img_keyword": "muscle growth", "sport": "Muscle Science", "series": "Muscle Growth Science", "episode": 1},
    {"title": "80% of Shoulder Pain Comes From This Muscle... You've Never Heard of It", "keyword": "serratus anterior weakness shoulder pain", "img_keyword": "shoulder pain", "sport": "Muscle Science", "series": "Upper Body Anatomy", "episode": 2},
    {"title": "Your Knee Hurts, So a Trainer Tells You to Work Your Glutes? Here's Why", "keyword": "gluteus medius knee pain pelvic balance", "img_keyword": "gluteus medius hip", "sport": "Muscle Science", "series": "Lower Body Anatomy", "episode": 2},
    {"title": "The Exercise You Must Do Before Your Knee Cartilage Wears Out", "keyword": "patellar tendinitis rehabilitation exercise", "img_keyword": "knee rehabilitation", "sport": "Rehab", "series": "Injury Rehab", "episode": 1},
    {"title": "3 Exercises You Should Never Do After a Herniated Disc Diagnosis", "keyword": "lumbar disc stabilization exercise", "img_keyword": "lower back pain", "sport": "Rehab", "series": "Injury Rehab", "episode": 2},
    {"title": "Iced Your Sprained Ankle Right Away? You Did It Wrong", "keyword": "ankle sprain rehabilitation return to sport", "img_keyword": "ankle sprain", "sport": "Rehab", "series": "Injury Rehab", "episode": 3},
    {"title": "Shoulder Impingement... What to Try at Home Before the Doctor", "keyword": "shoulder impingement home rehabilitation", "img_keyword": "shoulder impingement", "sport": "Rehab", "series": "Injury Rehab", "episode": 4},
    {"title": "If Your Achilles Hurts, Stretching It Is the Last Thing You Should Do", "keyword": "achilles tendinopathy exercise avoid", "img_keyword": "achilles tendon", "sport": "Rehab", "series": "Injury Rehab", "episode": 5},
    {"title": "What You Eat Before Training Can Change Your Performance by 50%", "keyword": "pre workout meal carbohydrate timing", "img_keyword": "pre workout meal", "sport": "Nutrition", "series": "Sports Nutrition Science", "episode": 1},
    {"title": "I Cut Carbs and My Performance Got Worse... Here's Why", "keyword": "carbohydrate glycogen sports performance", "img_keyword": "carbohydrate food", "sport": "Nutrition", "series": "Sports Nutrition Science", "episode": 2},
    {"title": "The Biggest Mistake People Make When Taking Creatine", "keyword": "creatine dosage timing supplement", "img_keyword": "creatine supplement", "sport": "Nutrition", "series": "Supplement Science", "episode": 1},
    {"title": "Drinking Only Water During Exercise Can Actually Cause Cramps", "keyword": "hydration during exercise timing amount", "img_keyword": "hydration water sports", "sport": "Nutrition", "series": "Sports Nutrition Science", "episode": 3},
    {"title": "How Much Protein Do You Really Need? Most Fitness Influencers Get It Wrong", "keyword": "protein daily intake calculation body weight", "img_keyword": "protein food", "sport": "Nutrition", "series": "Sports Nutrition Science", "episode": 4},
    {"title": "Eating Only Chicken Breast After a Workout Slows Down Your Recovery", "keyword": "post workout recovery nutrition combination", "img_keyword": "post workout nutrition", "sport": "Nutrition", "series": "Sports Nutrition Science", "episode": 5},
    {"title": "Some Athletes Thrive Under Pressure, Others Collapse... What's the Difference?", "keyword": "pre game routine anxiety control athletes", "img_keyword": "athlete focus", "sport": "Sports Psychology", "series": "Sports Psychology", "episode": 1},
    {"title": "What People Who Lose Focus Under Pressure All Have in Common", "keyword": "focus under pressure mental training sports", "img_keyword": "mental training", "sport": "Sports Psychology", "series": "Sports Psychology", "episode": 2},
    {"title": "Working Hard But Not Improving? It Might Be a Slump, Not Lack of Effort", "keyword": "sports slump recovery psychology steps", "img_keyword": "athlete motivation", "sport": "Sports Psychology", "series": "Sports Psychology", "episode": 3},
    {"title": "Can Mental Rehearsal Alone Actually Improve Your Performance?", "keyword": "mental imagery visualization sports performance", "img_keyword": "visualization meditation", "sport": "Sports Psychology", "series": "Sports Psychology", "episode": 4},
    {"title": "Why You Get Out of Breath So Fast... Lung Capacity vs Cardio Fitness", "keyword": "VO2max interval training intensity", "img_keyword": "interval running", "sport": "Conditioning", "series": "Conditioning Science", "episode": 1},
    {"title": "Why Marathon Runners Never Seem to Tire... The Truth About Lactate", "keyword": "lactate threshold training endurance", "img_keyword": "endurance running", "sport": "Conditioning", "series": "Conditioning Science", "episode": 2},
    {"title": "30 Minutes of HIIT and Still Not Losing Weight? Your Rest Periods Are the Problem", "keyword": "HIIT rest interval optimization fat loss", "img_keyword": "HIIT workout", "sport": "Conditioning", "series": "Cardio Science", "episode": 1},
    {"title": "Why Training With a Heart Rate Monitor Burns More Fat", "keyword": "heart rate zone exercise intensity training", "img_keyword": "heart rate monitor", "sport": "Conditioning", "series": "Conditioning Science", "episode": 3},
    {"title": "Is Stretching Before a Workout Actually Causing Your Injuries?", "keyword": "dynamic stretching warm up injury prevention", "img_keyword": "dynamic stretching", "sport": "Mobility", "series": "Mobility Science", "episode": 1},
    {"title": "Tight Hips Eventually Wreck Your Back, Knees, and Shoulders", "keyword": "hip flexor mobility stretching exercises", "img_keyword": "hip stretching", "sport": "Mobility", "series": "Mobility Revolution", "episode": 1},
    {"title": "Using a Foam Roller Wrong Can Actually Make Your Muscles Tighter", "keyword": "foam rolling myofascial release technique", "img_keyword": "foam roller", "sport": "Mobility", "series": "Recovery Science", "episode": 1},
    {"title": "If Your Shoulders Hurt, Your Upper Back Is Probably the Real Problem", "keyword": "thoracic spine mobility shoulder pain", "img_keyword": "spine mobility", "sport": "Mobility", "series": "Mobility Revolution", "episode": 2},
    {"title": "What Actually Happens Inside Your Muscles When You Work Out", "keyword": "muscle physiology exercise ATP energy", "img_keyword": "muscle exercise", "sport": "Physiology", "series": "Exercise Physiology", "episode": 1},
    {"title": "30 Minutes of Cardio and Still Not Burning Fat? Here's the Real Reason", "keyword": "fat oxidation aerobic exercise physiology", "img_keyword": "aerobic exercise", "sport": "Physiology", "series": "Exercise Physiology", "episode": 2},
    {"title": "Is It True That Your Muscles Grow While You Sleep?", "keyword": "growth hormone sleep muscle recovery", "img_keyword": "sleep recovery", "sport": "Physiology", "series": "Exercise Physiology", "episode": 3},
    {"title": "The Myth That More Soreness Means More Muscle Growth", "keyword": "DOMS delayed onset muscle soreness cause", "img_keyword": "muscle soreness", "sport": "Physiology", "series": "Exercise Physiology", "episode": 4},
    {"title": "Why an Athlete's Heart Is 50% Bigger Than a Regular Person's", "keyword": "cardiac adaptation exercise athlete heart", "img_keyword": "heart cardio", "sport": "Physiology", "series": "Exercise Physiology", "episode": 5},
    {"title": "Why High Stress Makes You Gain Fat and Lose Muscle at the Same Time", "keyword": "cortisol muscle loss stress hormone", "img_keyword": "stress cortisol", "sport": "Physiology", "series": "Exercise Physiology", "episode": 6},
    {"title": "If Your Shoulder Hurts, Why Does a PT Check Your Neck First?", "keyword": "shoulder pain physical therapy assessment", "img_keyword": "shoulder physical therapy", "sport": "Physical Therapy", "series": "PT Guide", "episode": 1},
    {"title": "Knee Pain: Signs That Mean See a Doctor vs Signs You Can Fix at Home", "keyword": "knee pain self diagnosis when to see doctor", "img_keyword": "knee pain", "sport": "Physical Therapy", "series": "PT Guide", "episode": 2},
    {"title": "You Don't Even Play Tennis, So Why Do You Have Tennis Elbow?", "keyword": "tennis elbow treatment home exercise", "img_keyword": "tennis elbow", "sport": "Physical Therapy", "series": "PT Guide", "episode": 3},
    {"title": "If Your Heels Hurt Every Morning, You're Missing This One Thing", "keyword": "plantar fasciitis morning stretching routine", "img_keyword": "plantar fasciitis foot", "sport": "Physical Therapy", "series": "PT Guide", "episode": 4},
    {"title": "Can 5 Minutes a Day Really Fix Forward Head Posture?", "keyword": "forward head posture correction exercise", "img_keyword": "neck posture", "sport": "Physical Therapy", "series": "PT Guide", "episode": 5},
    {"title": "If Your Knees Hurt When Running, You're Probably Making This Form Mistake", "keyword": "running biomechanics knee impact reduction", "img_keyword": "running form", "sport": "Biomechanics", "series": "Sports Biomechanics", "episode": 1},
    {"title": "Your Knees Cave In During Squats... It's Not Actually Your Knees' Fault", "keyword": "squat knee valgus cause biomechanics", "img_keyword": "squat form", "sport": "Biomechanics", "series": "Sports Biomechanics", "episode": 2},
    {"title": "People Who Hurt Their Back Deadlifting Never Understood Neutral Spine", "keyword": "deadlift spine neutral position injury prevention", "img_keyword": "deadlift", "sport": "Biomechanics", "series": "Sports Biomechanics", "episode": 3},
    {"title": "0.1 Seconds of Landing Decides Whether Your ACL Tears", "keyword": "landing mechanics ACL injury prevention", "img_keyword": "jump landing", "sport": "Biomechanics", "series": "Sports Biomechanics", "episode": 4},
    {"title": "Why Your Knees Get Injured So Often... It's Built Into the Structure", "keyword": "knee joint anatomy structure injury", "img_keyword": "knee joint", "sport": "Anatomy", "series": "Sports Anatomy", "episode": 1},
    {"title": "Your Shoulder Can Rotate 360 Degrees... and That's Exactly the Problem", "keyword": "shoulder joint anatomy mobility instability", "img_keyword": "shoulder joint", "sport": "Anatomy", "series": "Sports Anatomy", "episode": 2},
    {"title": "When Your Foot Arch Collapses, It Drags Down Your Knees, Back, and Neck Too", "keyword": "foot arch structure running performance", "img_keyword": "foot arch", "sport": "Anatomy", "series": "Sports Anatomy", "episode": 3},
    {"title": "One Sitting Posture Can Triple the Pressure on Your Spinal Discs", "keyword": "spinal disc anatomy pressure posture", "img_keyword": "spine disc", "sport": "Anatomy", "series": "Sports Anatomy", "episode": 4},
    {"title": "One Shoulder Lower Than the Other? Here's What Happens If You Ignore It", "keyword": "pelvic tilt imbalance lower back knee pain", "img_keyword": "pelvic posture", "sport": "Body Balance", "series": "Posture Correction", "episode": 1},
    {"title": "Scoliosis: A 5-Minute Self-Check You Can Do at Home", "keyword": "shoulder uneven scoliosis self check", "img_keyword": "scoliosis posture", "sport": "Body Balance", "series": "Posture Correction", "episode": 2},
    {"title": "What People With Flat Feet Need to Know Before They Train", "keyword": "flat feet sports performance correction", "img_keyword": "flat feet", "sport": "Body Balance", "series": "Posture Correction", "episode": 3},
    {"title": "Your Knees Hurt Because of Knock Knees, But You're Just Squatting Anyway?", "keyword": "knock knees correction gluteus medius", "img_keyword": "knock knees legs", "sport": "Body Balance", "series": "Posture Correction", "episode": 4},
    {"title": "Does Heavy Training in Youth Really Stunt a Child's Growth?", "keyword": "youth athlete growth plate safe training", "img_keyword": "youth sports training", "sport": "Sports Medicine", "series": "Sports Medicine Guide", "episode": 1},
    {"title": "The Warning Signs Before You Collapse From Heat During Summer Workouts", "keyword": "heat stroke warning signs summer exercise", "img_keyword": "heat stroke summer", "sport": "Sports Medicine", "series": "Sports Medicine Guide", "episode": 2},
    {"title": "Why Do You Suddenly Get Cramps During Exercise? It's Not Just Dehydration", "keyword": "exercise cramp cause prevention electrolyte", "img_keyword": "muscle cramp", "sport": "Sports Medicine", "series": "Sports Medicine Guide", "episode": 3},
    {"title": "Training Hard but Feeling Worse? The Signs of Overtraining", "keyword": "overtraining syndrome self check recovery", "img_keyword": "overtraining fatigue", "sport": "Sports Medicine", "series": "Sports Medicine Guide", "episode": 4},
    {"title": "Is It True That 7 Hours of Sleep Builds More Muscle?", "keyword": "sleep 7 hours muscle growth performance", "img_keyword": "sleep recovery", "sport": "General", "series": "Recovery Science", "episode": 1},
    {"title": "Is Losing Muscle With Age Really Unavoidable?", "keyword": "sarcopenia aging muscle loss prevention", "img_keyword": "aging fitness", "sport": "General", "series": "Senior Fitness", "episode": 1},
    {"title": "What Happens If Kids Start Serious Training Too Early?", "keyword": "youth sports age appropriate training", "img_keyword": "kids sports", "sport": "General", "series": "Youth Development", "episode": 1},
    {"title": "What People Who Quit Working Out After One Month All Have in Common", "keyword": "beginner exercise first month principles", "img_keyword": "beginner workout", "sport": "General", "series": "Fitness Foundations", "episode": 1},
    {"title": "Is It Actually Possible to Lose Fat and Gain Muscle at the Same Time?", "keyword": "body recomposition fat loss muscle gain", "img_keyword": "body recomposition", "sport": "General", "series": "Fitness Foundations", "episode": 2},
    {"title": "Tight Ankles Eventually Wreck Your Knees Too... Here's the Chain Reaction", "keyword": "soccer ankle mobility knee injury prevention", "img_keyword": "ankle mobility", "sport": "Soccer", "series": "Mobility Chain", "episode": 1},
    {"title": "Why Your Back Exercises Don't Work If Your Pelvis Is Tilted", "keyword": "pelvic tilt lumbar stabilization biomechanics", "img_keyword": "pelvic balance", "sport": "Body Balance", "series": "Mobility Chain", "episode": 2},
    {"title": "Bench Press Shoulder Pain Comes From a Stiff Upper Back, Not the Shoulder", "keyword": "thoracic mobility shoulder impingement bench press", "img_keyword": "bench press shoulder", "sport": "Mobility", "series": "Mobility Chain", "episode": 3},
    {"title": "Why Pitchers Lose Velocity When Their Hips Stop Rotating", "keyword": "hip rotation baseball pitching velocity anatomy", "img_keyword": "hip rotation pitcher", "sport": "Baseball", "series": "Mobility Chain", "episode": 4},
    {"title": "How a Collapsed Foot Arch Throws Off Your Entire Upper Body Balance", "keyword": "foot arch collapse upper body balance chain", "img_keyword": "foot arch balance", "sport": "Anatomy", "series": "Mobility Chain", "episode": 5},
    {"title": "Why the First Minute of HIIT Always Feels the Hardest", "keyword": "ATP-PC system lactate threshold HIIT physiology", "img_keyword": "HIIT training", "sport": "Physiology", "series": "Energy Science", "episode": 1},
    {"title": "Can Eating More Carbs the Night Before Really Make You Run Faster?", "keyword": "carbohydrate loading glycogen VO2max performance", "img_keyword": "carbohydrate loading", "sport": "Nutrition", "series": "Energy Science", "episode": 2},
    {"title": "The Worse the Soreness, the More Sleep You Actually Need", "keyword": "DOMS growth hormone sleep muscle protein synthesis", "img_keyword": "muscle recovery sleep", "sport": "Physiology", "series": "Energy Science", "episode": 3},
    {"title": "Is There Really a Heart Rate Zone Where Fat Burns Best?", "keyword": "fat oxidation aerobic heart rate zone science", "img_keyword": "fat burning cardio", "sport": "Conditioning", "series": "Energy Science", "episode": 4},
    {"title": "Why Working Out Doesn't Help When You're Already Stressed Out", "keyword": "cortisol muscle loss exercise slump physiology", "img_keyword": "stress hormone", "sport": "Physiology", "series": "Energy Science", "episode": 5},
    {"title": "Why Your Hamstring Only Tears While Sprinting... The Shocking Truth", "keyword": "hamstring eccentric contraction running biomechanics", "img_keyword": "hamstring running", "sport": "Rehab", "series": "Injury Chronicles", "episode": 1},
    {"title": "0.1 Seconds of Landing Mechanics That Tear Your ACL", "keyword": "ACL injury landing mechanics gluteus medius", "img_keyword": "ACL knee injury", "sport": "Biomechanics", "series": "Injury Chronicles", "episode": 2},
    {"title": "Morning Heel Pain Isn't About Your Foot... It's Your Calf", "keyword": "plantar fasciitis achilles tendinopathy connection", "img_keyword": "plantar fasciitis", "sport": "Physical Therapy", "series": "Injury Chronicles", "episode": 3},
    {"title": "Fixing Tennis Elbow Starts With Your Shoulder Blade, Not Your Wrist", "keyword": "tennis elbow scapular stability physical therapy", "img_keyword": "tennis elbow", "sport": "Physical Therapy", "series": "Injury Chronicles", "episode": 4},
    {"title": "Movements You Should Never Do While Recovering From a Herniated Disc", "keyword": "lumbar disc rehabilitation avoid movements", "img_keyword": "lumbar disc", "sport": "Rehab", "series": "Injury Chronicles", "episode": 5},
    {"title": "Sitting 8 Hours a Day Raises Injury Risk Even for Trained Athletes", "keyword": "forward head posture rotator cuff injury pitcher", "img_keyword": "neck posture office", "sport": "Body Balance", "series": "Office Athlete", "episode": 1},
    {"title": "Why Office Workers Hurt Their Back Squatting After Sitting All Day", "keyword": "transverse abdominis core squat back pain", "img_keyword": "core squat", "sport": "Muscle Science", "series": "Office Athlete", "episode": 2},
    {"title": "Sitting Too Long Can Make Your Glutes 'Forget' How to Work", "keyword": "psoas muscle gluteal amnesia reciprocal inhibition", "img_keyword": "hip flexor psoas", "sport": "Muscle Science", "series": "Office Athlete", "episode": 3},
    {"title": "The Real Reason Sitting 8 Hours a Day Tightens Your Hamstrings", "keyword": "sitting posture hamstring flexibility physiology", "img_keyword": "sitting hamstring", "sport": "Mobility", "series": "Office Athlete", "episode": 4},
    {"title": "What Separates Athletes Who Focus Better Under Pressure", "keyword": "focus under pressure attentional focus brain waves", "img_keyword": "athlete concentration", "sport": "Sports Psychology", "series": "Elite Mindset", "episode": 1},
    {"title": "Can Just Visualizing Movement Actually Activate Your Muscles?", "keyword": "mental imagery mirror neurons neuromuscular activation", "img_keyword": "mental visualization", "sport": "Sports Psychology", "series": "Elite Mindset", "episode": 2},
    {"title": "Trying to Calm Pre-Game Nerves Makes Them Worse... Here's Why", "keyword": "pre-game anxiety cognitive reappraisal sports", "img_keyword": "athlete pregame", "sport": "Sports Psychology", "series": "Elite Mindset", "episode": 3},
    {"title": "The One Mistake That Keeps Athletes Stuck in a Slump", "keyword": "sports slump recovery 3 steps psychology", "img_keyword": "sports motivation", "sport": "Sports Psychology", "series": "Elite Mindset", "episode": 4},
    {"title": "The Dangerous Signal Exercise Addicts Miss... When Dopamine Turns on You", "keyword": "exercise intensity dopamine overtraining mental", "img_keyword": "overtraining fatigue", "sport": "Sports Medicine", "series": "Elite Mindset", "episode": 5},
    {"title": "What Physical Therapists Won't Tell You First About Shoulder Pain", "keyword": "shoulder pain serratus anterior weakness", "img_keyword": "shoulder pain relief", "sport": "Physical Therapy", "series": "Pain Care", "episode": 1},
    {"title": "Sharp Pain in Front of Your Knee Going Down Stairs? Check This First", "keyword": "knee pain stairs patellar tendinitis", "img_keyword": "knee pain", "sport": "Physical Therapy", "series": "Pain Care", "episode": 2},
    {"title": "People Who Keep Spraining Their Ankles Are All Missing This One Sense", "keyword": "ankle sprain proprioception training", "img_keyword": "ankle stability", "sport": "Physical Therapy", "series": "Pain Care", "episode": 3},
    {"title": "Numb Arm but No Neck Disc Problem? You Might Have This Syndrome", "keyword": "thoracic outlet syndrome arm numbness", "img_keyword": "neck shoulder pain", "sport": "Physical Therapy", "series": "Pain Care", "episode": 4},
    {"title": "Stretches That Actually Make Lower Back Pain Worse", "keyword": "lower back pain stretching avoid", "img_keyword": "lower back pain", "sport": "Physical Therapy", "series": "Pain Care", "episode": 5},
    {"title": "Why Sitting 8 Hours a Day Tightens Your Hip Flexors... and What It Leads To", "keyword": "hip flexor tightness sitting office worker", "img_keyword": "office posture hip", "sport": "Body Balance", "series": "Desk Posture", "episode": 1},
    {"title": "Nobody Realizes Monitor Height Alone Can Cause Neck Pain", "keyword": "monitor height neck pain desk setup ergonomics", "img_keyword": "desk ergonomics monitor", "sport": "Body Balance", "series": "Desk Posture", "episode": 2},
    {"title": "One Sitting Adjustment That Cuts Lower Back Pain by Half", "keyword": "sitting posture lower back pain office chair", "img_keyword": "sitting posture office", "sport": "Body Balance", "series": "Desk Posture", "episode": 3},
    {"title": "The Common Mistake Behind Worsening Neck and Shoulder Pain From WFH", "keyword": "work from home neck shoulder stretch routine", "img_keyword": "neck stretch office", "sport": "Body Balance", "series": "Desk Posture", "episode": 4},
    {"title": "What People With Pain-Free Wrists Do Differently While Typing All Day", "keyword": "wrist pain typing keyboard ergonomics", "img_keyword": "wrist pain keyboard", "sport": "Physical Therapy", "series": "Desk Posture", "episode": 5},
    {"title": "Planking Every Day but Still Have Back Pain? It's Your Breathing", "keyword": "core weakness back pain transverse abdominis multifidus", "img_keyword": "core strength back", "sport": "Muscle Science", "series": "Core Strength", "episode": 1},
    {"title": "What People Who Get No Results From Core Workouts Are Missing", "keyword": "plank core activation breathing technique", "img_keyword": "plank exercise core", "sport": "Muscle Science", "series": "Core Strength", "episode": 2},
    {"title": "Where Should Someone With Belly Fat Start With Core Training?", "keyword": "belly fat core training beginner progression", "img_keyword": "core workout beginner", "sport": "Muscle Science", "series": "Core Strength", "episode": 3},
    {"title": "Why Dead Bugs Are One of the Best Exercises for Back Rehab", "keyword": "dead bug exercise lumbar rehabilitation core", "img_keyword": "dead bug core exercise", "sport": "Rehab", "series": "Core Strength", "episode": 4},
    {"title": "What Happens to Your Back and Knees If You Squat Without Core Stability", "keyword": "core stability squat lower back knee pain", "img_keyword": "squat core stability", "sport": "Muscle Science", "series": "Core Strength", "episode": 5},
    {"title": "Can't Stand on a Balance Pad for 10 Seconds? You Need This Now", "keyword": "balance pad ankle knee hip stability training", "img_keyword": "balance pad training", "sport": "Conditioning", "series": "Balance Tools", "episode": 1},
    {"title": "There's One Spot You Should Never Roll With a Foam Roller", "keyword": "foam roller technique correct usage avoid areas", "img_keyword": "foam roller technique", "sport": "Mobility", "series": "Balance Tools", "episode": 2},
    {"title": "Bosu Ball Training Isn't Just About Balance... Here's the Science", "keyword": "bosu ball core balance science effectiveness", "img_keyword": "bosu ball exercise", "sport": "Conditioning", "series": "Balance Tools", "episode": 3},
    {"title": "5 Stability Ball Exercises That Go From Rehab to Real Strength", "keyword": "stability ball back strengthening exercise rehabilitation", "img_keyword": "stability ball back exercise", "sport": "Rehab", "series": "Balance Tools", "episode": 4},
    {"title": "A Sliding Disc Routine That Hits Your Core and Lower Body Together", "keyword": "sliding disc core lower body exercise routine", "img_keyword": "sliding disc exercise", "sport": "Conditioning", "series": "Balance Tools", "episode": 5},
    {"title": "Choosing the Wrong Knee Brace Can Weaken Your Muscles Over Time", "keyword": "knee brace selection pain type guide", "img_keyword": "knee brace support", "sport": "Sports Medicine", "series": "Joint Protection", "episode": 1},
    {"title": "An Ankle Brace Can Actually Hurt Certain People... Are You One of Them?", "keyword": "ankle brace when to use avoid muscle weakness", "img_keyword": "ankle brace support", "sport": "Sports Medicine", "series": "Joint Protection", "episode": 2},
    {"title": "Wearing a Wrist Brace Alone Can Make Your Wrist Weaker", "keyword": "wrist support brace strengthening exercise", "img_keyword": "wrist support exercise", "sport": "Sports Medicine", "series": "Joint Protection", "episode": 3},
    {"title": "Taping vs Bracing... When You Should Actually Use Each", "keyword": "taping vs brace difference when to use sports", "img_keyword": "sports taping", "sport": "Sports Medicine", "series": "Joint Protection", "episode": 4},
    {"title": "A 30-Minute No-Equipment Routine That Beats the Gym", "keyword": "home workout no equipment full body strength routine", "img_keyword": "home workout", "sport": "General", "series": "Home Workout Solutions", "episode": 1},
    {"title": "How People Fixed Their Lower Back Pain With Just a Yoga Mat", "keyword": "yoga mat lower back pain relief routine", "img_keyword": "yoga mat back exercise", "sport": "Rehab", "series": "Home Workout Solutions", "episode": 2},
    {"title": "6 Resistance Band Exercises for Shoulders and Back When You Skip the Gym", "keyword": "resistance band upper body shoulder back exercise", "img_keyword": "resistance band exercise", "sport": "Muscle Science", "series": "Home Workout Solutions", "episode": 3},
    {"title": "Why 10 Minutes in the Morning Changes Your Posture for the Whole Day", "keyword": "morning routine posture improvement daily habit", "img_keyword": "morning stretch routine", "sport": "Body Balance", "series": "Home Workout Solutions", "episode": 4},
    {"title": "A 15-Minute Evening Routine to Undo a Whole Day of Tightness", "keyword": "foam roller massage ball recovery evening routine", "img_keyword": "foam roller recovery", "sport": "Mobility", "series": "Home Workout Solutions", "episode": 5},
    {"title": "The Real Cause of Bow Legs Isn't Your Legs... It's Your Glutes", "keyword": "bow legs hip external rotation correction cause", "img_keyword": "bow legs correction", "sport": "Body Balance", "series": "Advanced Posture Correction", "episode": 1},
    {"title": "Trying to Force Your Back Straight Can Make Rounded Shoulders Worse", "keyword": "kyphosis correction thoracic spine pectoral stretch", "img_keyword": "posture correction back", "sport": "Body Balance", "series": "Advanced Posture Correction", "episode": 2},
    {"title": "What Standing on One Leg for Years Does to Your Spine", "keyword": "weight shifting habit pelvic imbalance spine", "img_keyword": "posture balance standing", "sport": "Body Balance", "series": "Advanced Posture Correction", "episode": 3},
    {"title": "Is It True That Your Foot Shape Determines Your Whole Posture?", "keyword": "overpronation supination foot correction posture", "img_keyword": "foot pronation correction", "sport": "Body Balance", "series": "Advanced Posture Correction", "episode": 4},
    {"title": "Why an Anteriorly Tilted Pelvis Gives You a Permanent Belly Pooch", "keyword": "anterior pelvic tilt correction psoas abdominal", "img_keyword": "pelvic tilt exercise", "sport": "Body Balance", "series": "Advanced Posture Correction", "episode": 5},
]

USED_TOPICS_FILE = "used_topics.json"
SERIES_LINKS_FILE = "series_links.json"


def load_series_links():
    try:
        with open(SERIES_LINKS_FILE, "r") as f:
            return json.load(f)
    except Exception:
        return {}


def save_series_link(series, episode, title, url):
    links = load_series_links()
    if series not in links:
        links[series] = {}
    links[series][str(episode)] = {"title": title, "url": url}
    try:
        with open(SERIES_LINKS_FILE, "w") as f:
            json.dump(links, f, ensure_ascii=False)
        print("[Series Link] Saved: " + series + " episode " + str(episode))
    except Exception as e:
        print("[Series Link] Save failed: " + str(e))


def get_series_nav_html(topic):
    series = topic.get("series", "")
    episode = topic.get("episode", 1)
    if not series:
        return ""
    links = load_series_links()
    series_data = links.get(series, {})
    prev_html = ""
    next_html = ""
    prev_ep = str(episode - 1)
    if prev_ep in series_data:
        prev = series_data[prev_ep]
        prev_html = (
            '<a href="' + prev["url"] + '" style="display:flex;align-items:center;'
            'text-decoration:none;color:#1565c0;font-size:14px;font-weight:600;">'
            '◀ Previous: ' + prev["title"] + '</a>'
        )
    next_ep = str(episode + 1)
    if next_ep in series_data:
        nxt = series_data[next_ep]
        next_html = (
            '<a href="' + nxt["url"] + '" style="display:flex;align-items:center;'
            'text-decoration:none;color:#1565c0;font-size:14px;font-weight:600;">'
            'Next: ' + nxt["title"] + ' ▶</a>'
        )
    if not prev_html and not next_html:
        return ""
    html = (
        '<div style="background:#f0f4ff;border:2px solid #1565c0;border-radius:12px;'
        'padding:20px 24px;margin:40px 0;">'
        '<p style="font-weight:700;font-size:15px;color:#1565c0;margin-bottom:14px;">'
        '📚 More in the ' + series + ' series</p>'
        '<div style="display:flex;flex-direction:column;gap:10px;">'
    )
    if prev_html:
        html += '<div>' + prev_html + '</div>'
    if next_html:
        html += '<div>' + next_html + '</div>'
    html += '</div></div>\n'
    return html


def load_used_topics():
    try:
        with open(USED_TOPICS_FILE, "r") as f:
            return json.load(f)
    except Exception:
        return []


def save_used_topic(title):
    used = load_used_topics()
    used.append(title)
    if len(used) > 80:
        used = used[-80:]
    try:
        with open(USED_TOPICS_FILE, "w") as f:
            json.dump(used, f, ensure_ascii=False)
    except Exception as e:
        print("[Dedup] Save failed: " + str(e))


def pick_topic():
    used = load_used_topics()
    available = [t for t in TOPICS if t["title"] not in used]
    if not available:
        print("[Dedup] All topics used, resetting.")
        available = TOPICS
        try:
            with open(USED_TOPICS_FILE, "w") as f:
                json.dump([], f)
        except Exception:
            pass
    topic = random.choice(available)
    save_used_topic(topic["title"])
    return topic


def get_access_token():
    print("[Auth] Requesting Google Access Token...")
    response = requests.post(
        "https://oauth2.googleapis.com/token",
        data={
            "client_id": GOOGLE_CLIENT_ID,
            "client_secret": GOOGLE_CLIENT_SECRET,
            "refresh_token": GOOGLE_REFRESH_TOKEN,
            "grant_type": "refresh_token"
        },
        timeout=10
    )
    if response.status_code != 200:
        raise Exception("Token request failed: " + response.text)
    print("[Auth] Done!")
    return response.json()["access_token"]


def generate_with_claude(prompt):
    print("[AI] Calling Claude...")
    response = requests.post(
        "https://api.anthropic.com/v1/messages",
        headers={
            "x-api-key": ANTHROPIC_API_KEY,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json"
        },
        json={
            "model": "claude-sonnet-4-6",
            "max_tokens": 6000,
            "messages": [{"role": "user", "content": prompt}]
        },
        timeout=300
    )
    if response.status_code != 200:
        raise Exception("Claude error: " + str(response.status_code) + " " + response.text[:200])
    return response.json()["content"][0]["text"]


def generate_post():
    topic = pick_topic()
    print("[Generate] Topic: " + topic["title"])

    # ✅ 수정1: 등장인물 이름 랜덤화 (Marcus 고정 제거)
    client_names = ["Jake", "Sarah", "Tom", "David", "Elena", "James", "Nina", "Carlos", "Mia", "Ryan"]
    client_name = random.choice(client_names)

    series_info = ""
    if topic["episode"] > 1:
        series_info = (
            "This article is episode " + str(topic["episode"]) + " of the '" + topic["series"] + "' series. "
            + "Make it more advanced than the previous episode.\n\n"
        )

    prompt = (
        "You are a sports trainer and blogger with 10 years of hands-on experience.\n"
        "You explain complex sports science in a way anyone can understand,\n"
        "drawing on real stories from the gym floor and the field.\n"
        "Write only in English. Do not use any other language.\n"
        # ✅ 수정2: 이름 랜덤 지시
        "Use the client name \"" + client_name + "\" in your opening story, not always the same name.\n\n"
        + series_info
        + "## How to use the title\n"
        "The given title is a hook designed to spark curiosity.\n"
        "Your article must fully deliver on that hook - answer the question or claim in the title clearly within the body.\n\n"
        "## Core writing principles\n"
        "1. Open with a real scene from the gym or clinic - a story, not a definition.\n"
        "2. Structure it as a reveal: something the reader (or you) believed was wrong, and what's actually true.\n"
        "3. Explain technical concepts with everyday analogies. Example: 'Fascia is like the plastic wrap around your muscles.'\n"
        "4. For each subheading, follow this order: setup, then the science, then a real example, then what to do about it.\n"
        "5. End with one specific, concrete action the reader can try tomorrow.\n\n"
        "## Paragraph rules\n"
        "Each paragraph must be a dense block of 4-6+ sentences on one sub-idea.\n"
        "Never write one or two sentences and break the line. Only break paragraphs between sub-ideas.\n\n"
        "## Subheading rules\n"
        "Subheadings must use the format [emoji Subheading text], with exactly ONE emoji at the front only.\n"
        "Every subheading must include a specific number or data point.\n"
        "Good example: [\U0001f9b4 A 1-Degree Pelvic Tilt Triples the Pressure on Your Lower Back]\n"
        "Bad example: [\U0001f9b4 The Science of the Pelvis \U0001f9b4] (two emojis, no number)\n\n"
        "## Required elements\n"
        "Key concept: wrap one core concept in ##keyword## format and unpack it.\n"
        "Subheadings: at least 4, following the rules above.\n"
        "Training table: place between [TABLE_START] and [TABLE_END].\n"
        "Format: Exercise|Sets|Reps|Rest|Muscles Worked|Benefit\n"
        "[TABLE_START]\n"
        "Exercise|Sets|Reps|Rest|Muscles Worked|Benefit\n"
        "Example|3|12 reps|60 sec|Quadriceps|Lower body strength\n"
        "[TABLE_END]\n"
        "Summary: 3 lines with numbers, between [SUMMARY_START] and [SUMMARY_END].\n\n"
        "Length: 4000-6000 characters. Go deep, don't pad with filler.\n"
        "Avoid generic AI-sounding phrasing. Friendly but knowledgeable tone - like a trainer talking to a client.\n\n"
        "Category: " + topic["sport"] + "\n"
        "Topic title: " + topic["title"] + "\n\n"
        "Output format:\n"
        "Title: (a sharpened, even more compelling version of the topic title)\n"
        "---\n"
        "(article body)"
    )

    full_text = generate_with_claude(prompt)

    lines = full_text.strip().split("\n")
    title = ""
    body_lines = []
    separator_found = False

    for line in lines:
        if line.startswith("Title:"):
            title = line.replace("Title:", "").strip()
        elif line.strip() == "---":
            separator_found = True
        elif separator_found:
            body_lines.append(line)

    body = "\n".join(body_lines).strip()
    if not title:
        title = topic["title"]
    if not body:
        body = full_text

    print("[Done] Title: " + title)
    print("[Done] Length: " + str(len(body)) + " chars")
    return {"title": title, "body": body, "topic": topic}


def get_images_unsplash(keyword, count=3):
    if not UNSPLASH_ACCESS_KEY:
        return []
    try:
        response = requests.get(
            "https://api.unsplash.com/search/photos",
            params={
                "query": keyword,
                "per_page": 10,
                "page": random.randint(1, 3),
                "orientation": "landscape",
                "client_id": UNSPLASH_ACCESS_KEY
            },
            timeout=10
        )
        if response.status_code == 200:
            images = []
            for photo in response.json().get("results", []):
                images.append({
                    "url": photo["urls"]["regular"],
                    "alt": photo.get("alt_description", keyword) or keyword,
                    "author": photo["user"]["name"],
                    "author_url": photo["user"]["links"]["html"],
                    "source": "Unsplash"
                })
            random.shuffle(images)
            return images[:count]
    except Exception as e:
        print("[Unsplash error] " + str(e))
    return []


def get_images_pexels(keyword, count=3):
    pexels_key = os.environ.get("PEXELS_API_KEY", "")
    if not pexels_key:
        return []
    try:
        response = requests.get(
            "https://api.pexels.com/v1/search",
            headers={"Authorization": pexels_key},
            params={"query": keyword, "per_page": count, "orientation": "landscape"},
            timeout=10
        )
        if response.status_code == 200:
            images = []
            for photo in response.json().get("photos", []):
                images.append({
                    "url": photo["src"]["large"],
                    "alt": photo.get("alt", keyword) or keyword,
                    "author": photo["photographer"],
                    "author_url": photo["photographer_url"],
                    "source": "Pexels"
                })
            return images
    except Exception as e:
        print("[Pexels error] " + str(e))
    return []


def get_images_pixabay(keyword, count=3):
    pixabay_key = os.environ.get("PIXABAY_API_KEY", "")
    if not pixabay_key:
        return []
    try:
        response = requests.get(
            "https://pixabay.com/api/",
            params={
                "key": pixabay_key,
                "q": keyword,
                "image_type": "photo",
                "orientation": "horizontal",
                "per_page": count,
                "safesearch": "true"
            },
            timeout=10
        )
        if response.status_code == 200:
            images = []
            for hit in response.json().get("hits", []):
                images.append({
                    "url": hit["webformatURL"],
                    "alt": keyword,
                    "author": hit["user"],
                    "author_url": "https://pixabay.com/users/" + hit["user"] + "-" + str(hit["user_id"]),
                    "source": "Pixabay"
                })
            return images
    except Exception as e:
        print("[Pixabay error] " + str(e))
    return []


def get_images(keyword, count=3):
    print("[Image search] keyword: " + keyword)
    images = get_images_unsplash(keyword, count)
    if images:
        print("[Image] Unsplash " + str(len(images)) + " photos")
        return images
    images = get_images_pexels(keyword, count)
    if images:
        print("[Image] Pexels " + str(len(images)) + " photos")
        return images
    images = get_images_pixabay(keyword, count)
    if images:
        print("[Image] Pixabay " + str(len(images)) + " photos")
        return images
    print("[Image] All sources failed")
    return []


def make_table_html(table_text):
    rows = [r.strip() for r in table_text.strip().split("\n") if r.strip()]
    if not rows:
        return ""
    html = '<div style="overflow-x:auto;margin:24px 0;">'
    html += '<table style="width:100%;border-collapse:collapse;font-size:15px;">'
    for i, row in enumerate(rows):
        cols = row.split("|")
        html += "<tr>"
        for col in cols:
            if i == 0:
                html += '<th style="background:#1565c0;color:#fff;padding:10px 14px;text-align:center;border:1px solid #1565c0;">' + col.strip() + "</th>"
            else:
                bg = "#f5f8ff" if i % 2 == 0 else "#ffffff"
                html += '<td style="padding:9px 14px;text-align:center;border:1px solid #dde3f0;background:' + bg + ';">' + col.strip() + "</td>"
        html += "</tr>"
    html += "</table></div>\n"
    return html


def make_summary_html(summary_text):
    lines = [l.strip() for l in summary_text.strip().split("\n") if l.strip()]
    html = '<div style="background:#e8f4fd;border-left:5px solid #1565c0;border-radius:8px;padding:20px 24px;margin:28px 0;">'
    html += '<p style="font-weight:700;font-size:17px;color:#1565c0;margin-bottom:12px;">📌 Key Takeaways</p>'
    for line in lines:
        html += '<p style="margin:6px 0;font-size:15px;color:#333;">✅ ' + line + "</p>"
    html += "</div>\n"
    return html


def make_image_html(img, margin_top="0"):
    source = img.get("source", "Unsplash")
    html = '<div style="text-align:center;margin:30px 0;margin-top:' + margin_top + ';">'
    html += '<img src="' + img["url"] + '" alt="' + img["alt"] + '" style="max-width:100%;border-radius:10px;box-shadow:0 4px 12px rgba(0,0,0,0.12);"/>'
    html += '<p style="font-size:12px;color:#999;margin-top:8px;">Photo by <a href="' + img["author_url"] + '" style="color:#999;">' + img["author"] + '</a> on ' + source + '</p>'
    html += "</div>\n"
    return html


def body_to_html(body, images, topic):
    sport_emoji = SPORT_EMOJI.get(topic["sport"], "🏆")

    series_badge = ""
    if topic.get("series"):
        series_badge = (
            '<div style="display:inline-block;background:#1565c0;color:#fff;'
            'font-size:13px;padding:5px 14px;border-radius:20px;margin-bottom:20px;font-weight:600;">'
            + sport_emoji + " " + topic["series"] + " - Part " + str(topic["episode"]) + "</div>\n"
        )

    html = series_badge

    if len(images) >= 1:
        html += make_image_html(images[0])

    table_pattern = re.compile(r'\[TABLE_START\](.*?)\[TABLE_END\]', re.DOTALL)
    summary_pattern = re.compile(r'\[SUMMARY_START\](.*?)\[SUMMARY_END\]', re.DOTALL)

    table_match = table_pattern.search(body)
    summary_match = summary_pattern.search(body)

    table_html = make_table_html(table_match.group(1)) if table_match else ""
    summary_html = make_summary_html(summary_match.group(1)) if summary_match else ""

    clean_body = table_pattern.sub("[TABLE_PLACEHOLDER]", body)
    clean_body = summary_pattern.sub("[SUMMARY_PLACEHOLDER]", clean_body)

    headings = re.findall(r'\[([^\]]+)\]', clean_body)
    headings = [h for h in headings if h not in ["TABLE_PLACEHOLDER", "SUMMARY_PLACEHOLDER"]]
    if headings:
        toc = '<div style="background:#f8f9ff;border:1px solid #dde3f0;border-radius:10px;padding:20px 24px;margin:24px 0;">'
        toc += '<p style="font-weight:700;font-size:15px;color:#1565c0;margin-bottom:12px;">📋 Table of Contents</p>'
        toc += '<ol style="margin:0;padding-left:20px;">'
        for h in headings:
            clean_h = re.sub(r'^[^\w]+', '', h).strip()
            toc += '<li style="margin:6px 0;font-size:15px;color:#444;line-height:1.6;">' + clean_h + '</li>'
        toc += '</ol></div>\n'
        html += toc

    keyword_pattern = re.compile(r'##(.+?)##')
    def replace_keyword(m):
        return (
            '<span style="display:inline-block;font-size:28px;font-weight:900;'
            'color:#1565c0;letter-spacing:-0.5px;margin:20px 0 8px 0;'
            'border-bottom:3px solid #1565c0;padding-bottom:4px;">'
            + m.group(1) + '</span>'
        )

    paragraphs = clean_body.split("\n")
    mid = len(paragraphs) // 2
    image2_inserted = False
    para_count = 0

    for i, para in enumerate(paragraphs):
        if not para.strip():
            continue
        if para.strip() == "[TABLE_PLACEHOLDER]":
            html += table_html
            continue
        if para.strip() == "[SUMMARY_PLACEHOLDER]":
            html += summary_html
            continue
        if para.startswith("[") and "]" in para:
            heading = para.strip("[]").strip()
            html += (
                '<h2 style="margin-top:48px;margin-bottom:16px;font-size:22px;font-weight:700;'
                'background:linear-gradient(90deg,#1565c0,#1976d2);'
                'color:#fff;padding:12px 20px;border-radius:8px;">'
                + heading + "</h2>\n"
            )
            continue
        if len(para.strip()) > 1 and para.strip()[0].isdigit() and para.strip()[1] in [".", ")"]:
            html += (
                '<div style="display:flex;align-items:flex-start;margin:10px 0;padding:12px 16px;'
                'background:#f5f8ff;border-radius:8px;">'
                '<span style="color:#1565c0;font-weight:700;margin-right:12px;font-size:16px;">'
                + para.strip()[0] + '.</span>'
                '<span style="color:#333;font-size:16px;line-height:1.8;">'
                + para.strip()[2:].strip() + '</span></div>\n'
            )
            continue
        para_count += 1
        processed = keyword_pattern.sub(replace_keyword, para.strip())
        if processed != para.strip():
            html += '<div style="margin:28px 0 12px 0;">' + processed + '</div>\n'
        elif para_count % 4 == 0 and len(para.strip()) > 30:
            html += (
                '<div style="border-left:4px solid #1565c0;padding:14px 20px;margin:20px 0;'
                'background:#f0f4ff;border-radius:0 8px 8px 0;">'
                '<p style="margin:0;font-size:16px;line-height:1.9;color:#1a1a2e;font-weight:500;">'
                + para.strip() + '</p></div>\n'
            )
        else:
            html += (
                '<p style="margin:0 0 20px 0;line-height:2.0;font-size:16px;color:#333;text-align:justify;">'
                + para.strip() + '</p>\n'
            )
        if i >= mid and not image2_inserted and len(images) >= 2:
            html += make_image_html(images[1], margin_top="20px")
            image2_inserted = True

    if len(images) >= 3:
        html += make_image_html(images[2], margin_top="20px")

    html += get_series_nav_html(topic)
    return html


def request_google_indexing(post_url):
    import json as json_lib, time, base64
    service_account_json = os.environ.get("GOOGLE_SERVICE_ACCOUNT_JSON", "")
    if not service_account_json:
        print("[Indexing] GOOGLE_SERVICE_ACCOUNT_JSON not set - skipping")
        return
    try:
        sa_info = json_lib.loads(service_account_json)
        now = int(time.time())
        header = base64.urlsafe_b64encode(
            json_lib.dumps({"alg": "RS256", "typ": "JWT"}).encode()
        ).rstrip(b"=").decode()
        payload_data = {
            "iss": sa_info["client_email"],
            "scope": "https://www.googleapis.com/auth/indexing",
            "aud": "https://oauth2.googleapis.com/token",
            "exp": now + 3600,
            "iat": now
        }
        payload_b64 = base64.urlsafe_b64encode(
            json_lib.dumps(payload_data).encode()
        ).rstrip(b"=").decode()
        from cryptography.hazmat.primitives import hashes, serialization
        from cryptography.hazmat.primitives.asymmetric import padding
        private_key = serialization.load_pem_private_key(
            sa_info["private_key"].encode(), password=None
        )
        sign_input = (header + "." + payload_b64).encode()
        signature = private_key.sign(sign_input, padding.PKCS1v15(), hashes.SHA256())
        jwt_token = header + "." + payload_b64 + "." + base64.urlsafe_b64encode(signature).rstrip(b"=").decode()
        token_response = requests.post(
            "https://oauth2.googleapis.com/token",
            data={"grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer", "assertion": jwt_token},
            timeout=10
        )
        if token_response.status_code != 200:
            print("[Indexing] Token request failed: " + token_response.text[:200])
            return
        access_token = token_response.json().get("access_token", "")
        index_response = requests.post(
            "https://indexing.googleapis.com/v3/urlNotifications:publish",
            headers={"Authorization": "Bearer " + access_token, "Content-Type": "application/json"},
            json={"url": post_url, "type": "URL_UPDATED"},
            timeout=10
        )
        if index_response.status_code == 200:
            print("[Indexing] Request sent successfully! ✅ " + post_url)
        else:
            print("[Indexing] Request failed: " + index_response.text[:200])
    except Exception as e:
        print("[Indexing error] " + str(e))


def send_telegram(title, post_url, topic):
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        return
    sport_emoji = SPORT_EMOJI.get(topic["sport"], "🏆")
    message = sport_emoji + " New post\n\n📌 " + title + "\n\n🔗 " + post_url
    try:
        response = requests.post(
            "https://api.telegram.org/bot" + TELEGRAM_BOT_TOKEN + "/sendMessage",
            json={"chat_id": TELEGRAM_CHAT_ID, "text": message},
            timeout=10
        )
        if response.status_code == 200:
            print("[Telegram] Sent!")
        else:
            print("[Telegram] Failed: " + response.text[:200])
    except Exception as e:
        print("[Telegram error] " + str(e))


def send_facebook(title, post_url, topic):
    if not FACEBOOK_PAGE_ID or not FACEBOOK_ACCESS_TOKEN:
        return
    sport_emoji = SPORT_EMOJI.get(topic["sport"], "🏆")
    message = sport_emoji + " " + title + "\n\nRead more 👉 " + post_url
    try:
        response = requests.post(
            "https://graph.facebook.com/v19.0/" + FACEBOOK_PAGE_ID + "/feed",
            data={"message": message, "link": post_url, "access_token": FACEBOOK_ACCESS_TOKEN},
            timeout=10
        )
        if response.status_code == 200:
            print("[Facebook] Shared!")
        else:
            print("[Facebook] Failed: " + response.text[:200])
    except Exception as e:
        print("[Facebook error] " + str(e))


def send_instagram(title, post_url, image_url, topic):
    instagram_account_id = os.environ.get("INSTAGRAM_ACCOUNT_ID", "")
    if not instagram_account_id or not FACEBOOK_ACCESS_TOKEN:
        return
    if not image_url:
        print("[Instagram] No image, skipping")
        return
    sport_emoji = SPORT_EMOJI.get(topic["sport"], "🏆")
    caption = sport_emoji + " " + title + "\n\nRead more 👉 " + post_url
    try:
        r1 = requests.post(
            "https://graph.facebook.com/v19.0/" + instagram_account_id + "/media",
            data={"image_url": image_url, "caption": caption, "access_token": FACEBOOK_ACCESS_TOKEN},
            timeout=30
        )
        if r1.status_code != 200:
            print("[Instagram] Container failed: " + r1.text[:200])
            return
        creation_id = r1.json().get("id", "")
        if not creation_id:
            print("[Instagram] No creation_id")
            return
        r2 = requests.post(
            "https://graph.facebook.com/v19.0/" + instagram_account_id + "/media_publish",
            data={"creation_id": creation_id, "access_token": FACEBOOK_ACCESS_TOKEN},
            timeout=30
        )
        if r2.status_code == 200:
            print("[Instagram] Shared!")
        else:
            print("[Instagram] Publish failed: " + r2.text[:200])
    except Exception as e:
        print("[Instagram error] " + str(e))


def post_to_blogger(post_data, images, retry=2):
    print("\n[Blogger] Starting post...")
    topic = post_data["topic"]
    # ✅ 수정3: 시리즈 태그 제거, 카테고리만 유지
    labels = [topic["sport"]]

    for attempt in range(1, retry + 2):
        try:
            access_token = get_access_token()
            body_html = body_to_html(post_data["body"], images, topic)
            url = "https://www.googleapis.com/blogger/v3/blogs/" + BLOG_ID + "/posts?isDraft=false"
            headers = {
                "Authorization": "Bearer " + access_token,
                "Content-Type": "application/json"
            }
            payload = {
                "kind": "blogger#post",
                "title": post_data["title"],
                "content": body_html,
                "labels": labels,
                "status": "LIVE"
            }
            print("[Attempt " + str(attempt) + "] Title: " + post_data["title"])
            response = requests.post(url, headers=headers, json=payload, timeout=30)
            print("[Response] Status code: " + str(response.status_code))
            if response.status_code == 200:
                result = response.json()
                post_url = result.get("url", "")
                print("\nPublished!")
                print("   URL: " + post_url)
                save_series_link(topic.get("series", ""), topic.get("episode", 1), post_data["title"], post_url)
                request_google_indexing(post_url)
                send_telegram(post_data["title"], post_url, topic)
                send_facebook(post_data["title"], post_url, topic)
                image_url = images[0]["url"] if images else ""
                send_instagram(post_data["title"], post_url, image_url, topic)
                return True
            else:
                print("Failed: " + response.text[:300])
                if attempt <= retry:
                    print("[Retry] attempt " + str(attempt) + "...")
        except Exception as e:
            print("[Error] " + str(e))
            if attempt <= retry:
                print("[Retry] attempt " + str(attempt) + "...")
    return False


if __name__ == "__main__":
    print("=" * 50)
    print("AutoBlog Sports Publisher - Claude Edition (English)")
    print("Run time: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print("=" * 50)
    try:
        post = generate_post()
        images = get_images(post["topic"].get("img_keyword", post["topic"]["keyword"]), count=3)
        post_to_blogger(post, images)
        print("\nAll done!")
    except Exception as e:
        print("\nError: " + str(e))
        import traceback
        traceback.print_exc()
        exit(1)
