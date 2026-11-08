"""Recurring series, filming setups and the fixed daily routine."""

# Weekday -> series. Every day's anchor post is built around the rep of the day.
SERIES = {
    "Mon": dict(name="REP DROP", fmt="Reel, 20-35s", time="11:30 AM",
                why="Kick off the week. Show the app, read the rep, react, do it, invite. The signature format.",
                setup="A + D"),
    "Tue": dict(name="REP IN THE WILD", fmt="Reel, 15-30s", time="11:30 AM",
                why="Do the rep out in real life: coffee shop, office, car line, grocery store. Candid, funny, proof it fits a normal day.",
                setup="C"),
    "Wed": dict(name="WHY THIS REP WORKS", fmt="Carousel, 7 slides (4:5)", time="8:00 AM",
                why="The InnerBoard thinking behind the rep. Built to be saved and DM'd to a rep partner.",
                setup="G"),
    "Thu": dict(name="REP DUET", fmt="Collab Reel, 20-40s", time="11:30 AM",
                why="Do the rep with a guest (friend, client, teammate, family). Invite them as a Collaborator so it hits both audiences.",
                setup="F"),
    "Fri": dict(name="ROLL CALL", fmt="Reel montage, 20-40s", time="11:30 AM",
                why="Celebrate the Rep Crew by name. Their stories, comments and DMs are the content. Being seen is the reward.",
                setup="A + D"),
    "Sat": dict(name="LIFE LOOKS GOOD", fmt="Lifestyle Reel, 10-20s, trending audio", time="10:00 AM",
                why="Make life sexy. Golden-hour, merch, joy, the ordinary moment made beautiful. Reach beyond the growth crowd.",
                setup="E"),
    "Sun": dict(name="SET THE WEEK", fmt="IG Live + Facebook Group Live, 20 min; then a 30s clip", time="7:00 PM Live",
                why="Mirrors the app's Sunday 'Set the Week'. Live with the crew, preview the week, pick one rep together.",
                setup="H"),
}

SETUPS = {
    "A": ("Kitchen Counter", [
        "Phone on tripod at eye level, vertical 9:16, 4K 30fps, back camera (use a flip mirror or the Edits app preview).",
        "Face a window, light at 45 degrees. Cream wall or open shelves behind you. Gold mug or flowers in frame.",
        "Clip-on mic (DJI Mic or similar). Frame chest-up with headroom for captions.",
        "Talk to one person in the lens. First line within the first second, no 'hey guys'.",
    ]),
    "B": ("Car Confessional", [
        "Parked. Phone on dash or vent mount, facing a side window for soft light.",
        "Best for raw, honest reps and 'I almost didn't do this one' energy. Engine off, AC off for sound.",
    ]),
    "C": ("In the Wild", [
        "Handheld at arm's length, 1x lens (0.5x distorts faces), or hand the phone to a friend.",
        "Grab 3 shots: you arriving (wide), you doing the rep (medium), your reaction after (close).",
        "Wind muff on the mic outdoors. Ask permission before filming anyone's face; film hands, backs or reactions otherwise.",
    ]),
    "D": ("App POV", [
        "Screen-record the real Practice app: notification, Today's Rep screen, the tap to complete (Control Center > Screen Recording).",
        "Plus an over-the-shoulder shot of your thumb opening the notification with coffee in the other hand.",
        "Always real app footage. Never simulate a coaching response.",
    ]),
    "E": ("Golden Hour Lifestyle", [
        "The hour before sunset. Shoot 6-10 B-roll clips of 3-5 seconds each; 60fps for slow motion.",
        "Wear the merch (Club Hoodie, Life Takes Reps cap). Movement in every clip: walking, laughing, pouring, spinning.",
        "Edit to a trending audio in the Edits app or CapCut; one line of on-screen text, no talking needed.",
    ]),
    "F": ("Two-Shot Duet", [
        "Two people on a couch or at the counter. Phone vertical, a step further back, both faces in frame.",
        "Two mics if you have them. Film the 'before rep' take and the 'after rep' take for contrast.",
        "Add the guest as a Collaborator when posting.",
    ]),
    "G": ("Carousel Design", [
        "Canva template, 1080x1350 (4:5). Cream background, navy serif headline, one gold italic phrase per slide.",
        "Slide 1 is the hook. Slide 6 asks for the send. Slide 7 is the end card. Max 25 words a slide.",
        "Batch these on Sunday afternoons: they don't depend on the morning's rep.",
    ]),
    "H": ("Live", [
        "Phone on tripod, light in front of you, quiet room. Go Live on Instagram; a second phone runs Facebook Group Live (or go live in the Group right after).",
        "20 minutes: 3 min welcome + wins, 7 min the week's theme, 7 min pick and do a rep together live, 3 min invite.",
        "Save the replay. Cut the best 30s into Monday's story and the Facebook Group.",
    ]),
}

DAILY_ROUTINE = [
    ("7:00 AM", "Morning Drop (Story)",
     "Screenshot the app's Today's Rep. Add an 'Add Yours' sticker with the rep text and a poll: 'You in?' IN / Tomorrow. "
     "Add a question box: 'Who do you choose to be today?' Send the rep to the IG Broadcast Channel (The Rep Crew)."),
    ("7:05 AM", "Facebook Group thread",
     "Post the rep as the day's thread in The Practice Club: Rep Room. 'Today's rep: ___. Who's in? Drop IN.'"),
    ("7:15 AM", "Film (15 min)",
     "Film today's anchor post using the day's setup and shot list. If the app's rep is different from the backup rep below, use the app's rep. The format works for any rep."),
    ("Post time", "Anchor post",
     "Publish the anchor post at the series time. Crosspost Reels to Facebook Reels. Pin the best comment."),
    ("First 60 min", "Engagement block (30 min)",
     "Reply to every comment. Heart and cheer every IN. DM the link to anyone who asks. Comment thoughtfully on 5 creators from the intel list and 5 Rep Crew members."),
    ("Midday", "Doing-it Story (1-3 frames)",
     "Raw behind-the-scenes of you actually doing the rep. No polish. Tag #RepWithMe."),
    ("7:00 PM", "Close the Day (Story)",
     "Reshare every Rep Crew tag and Add Yours entry. Question box: 'Your three: what went well today?' Mirrors the app's Close the Day."),
    ("Weekly, Sunday afternoon", "Batch (60-90 min)",
     "Design Wednesday's carousel, line up Thursday's duet guest, pick Saturday's location and outfit, log last week's numbers in the tracker."),
]

FUN_RULES = [
    "React honestly when you read the rep. 'Oh, this one's spicy' is better than a lesson.",
    "Exaggerate the human moment: the most dramatic breath, the longest pause, the biggest no.",
    "Let the app be a character. 'My app is bossing me around again.'",
    "Always end with the invitation, never the lecture: 'Do it with me. Comment IN.'",
    "Same closing line every day so it becomes a chant: 'Life takes reps. See you tomorrow.'",
]

GROWTH_ENGINE = [
    ("Comment-to-DM automation",
     "Every anchor post ends with 'Comment IN'. Use a Meta-approved DM automation tool (ManyChat or Meta's built-in auto-replies) to DM the app link to every IN. Confirm the Practice app URL first."),
    ("IG Broadcast Channel: The Rep Crew",
     "One message every morning with the rep and a voice note. The most loyal 1% live here."),
    ("Facebook Group: The Practice Club, Rep Room",
     "Daily rep thread, Sunday Live, Friday wins thread. Moms of teens and practice owners are on Facebook."),
    ("Add Yours chain",
     "The rep travels follower to follower through the Add Yours sticker every morning."),
    ("Collabs every Thursday",
     "Four guests a month, each posting to their audience. Start with clients you're already inviting to Supercharge in Fort Lauderdale."),
    ("Rep of the Month",
     "Each month one Rep Crew member gets a Life Takes Reps cap, announced on the last Friday. Gives people a reason to tag you."),
    ("Repurpose the show",
     "Cut your Dr. Pat Show episodes into 30-45s clips with a hook line on screen. One per week as a bonus post."),
    ("Rep counter",
     "Track IN comments + story tags + app completions. Show the running total every Friday. Road to 10,000 reps."),
]
