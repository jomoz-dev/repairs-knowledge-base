from datetime import date

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from knowledge.models import Article, Category

DEFAULT_REVIEWED_ON = date(2026, 10, 1)
DEFAULT_REVIEWED_BY = "Housing Repairs Coordinator"

CATEGORIES = [
    {
        "name": "Call handling",
        "slug": "call-handling",
        "summary": "Who to send, gas emergency, and finding the stopcock before anyone attends.",
        "typical_trades": "Depends on the defect",
        "sort_order": 0,
    },
    {
        "name": "Water leak",
        "slug": "water-leak",
        "summary": "Active leaks, contained water, and cases where water may have reached electrics.",
        "typical_trades": "Plumber, Plumber / Electrician",
        "sort_order": 1,
    },
    {
        "name": "Electrical",
        "slug": "electrical",
        "summary": "Sparking, burning smell, power loss and unsafe fittings.",
        "typical_trades": "Electrician",
        "sort_order": 2,
    },
    {
        "name": "Heating",
        "slug": "heating",
        "summary": "No heating, no hot water, and vulnerability that changes attendance.",
        "typical_trades": "Heating Engineer",
        "sort_order": 3,
    },
    {
        "name": "Damp and mould",
        "slug": "damp-and-mould",
        "summary": "Visible mould, long-standing damp, children under 5 and respiratory risk.",
        "typical_trades": "Damp Specialist",
        "sort_order": 4,
    },
    {
        "name": "Roofing",
        "slug": "roofing",
        "summary": "Water entering through the roof, structural concern, electrics at risk.",
        "typical_trades": "Roofer",
        "sort_order": 5,
    },
    {
        "name": "Doors and windows",
        "slug": "doors-and-windows",
        "summary": "Insecure doors, windows that will not close, lock and joinery faults.",
        "typical_trades": "Locksmith, Joiner",
        "sort_order": 6,
    },
]

ARTICLES = [
    {
        "category": "call-handling",
        "title": "Who to send — trade and priority at a glance",
        "slug": "who-to-send",
        "audience": Article.AUDIENCE_ADVISOR,
        "related_priority": Article.PRIORITY_MIXED,
        "summary": "Match the defect to the trade before you raise the works order. Wrong trade means a wasted visit.",
        "body": """Use this with the diagnostic tool. The questions decide Emergency / Urgent / Routine. This list decides who attends.

Water on sockets, lights or the consumer unit: Plumber / Electrician, Emergency.

Active leak that cannot be contained, or is entering a neighbour: Plumber, Emergency.

Contained leak still running: Plumber, Urgent.

Sparking, burning smell or a hot scorched fitting: Electrician, Emergency.

Whole-property power loss with no burning: Electrician, Urgent. Check whether the neighbour still has power.

Smell of gas: do not book a heating engineer. Give the National Gas Emergency number 0800 111 999 and log that you did.

No heating and a vulnerable resident: Heating Engineer, Emergency.

No heating, or no hot water, without that vulnerability: Heating Engineer, Urgent.

Visible mould with a child under 5, a respiratory condition, or present for more than 28 days: Damp Specialist, Urgent.

Water entering through the roof and wet loft electrics: Roofer, Emergency, and flag electrical risk.

Water entering, or structural roof concern, without wet electrics: Roofer, Urgent.

Door that cannot be secured, or a window that cannot be closed: Locksmith or Joiner, Urgent. After a break-in or a communal door on the latch: Locksmith, Emergency.

If two trades are needed, raise two clear orders rather than one vague job. Record why you chose the trade so the next user can see it.""",
    },
    {
        "category": "call-handling",
        "title": "Smell of gas — not a heating diary job",
        "slug": "smell-of-gas",
        "audience": Article.AUDIENCE_ADVISOR,
        "related_priority": Article.PRIORITY_EMERGENCY,
        "summary": "Gas emergency first. Do not send a routine heating engineer until the supply is declared safe.",
        "body": """If the resident reports a gas smell, treat it as a gas emergency, not a boiler repair.

Give them 0800 111 999 (National Gas Emergency Service). Stay on the line until they confirm they will call, or call with them if they cannot.

Tell them: open windows, do not use light switches or the doorbell if the smell is strong, do not smoke, and turn the gas off at the meter only if they know how and it is safe to reach.

Log the time, the number you gave, and whether they were able to call. Do not raise a heating works order in parallel until the emergency service or network operator says the supply is safe.

Once it is safe, you can log a follow-on heating inspection if the appliance still needs a landlord engineer.""",
    },
    {
        "category": "call-handling",
        "title": "Resident: if you can smell gas",
        "slug": "resident-smell-of-gas",
        "audience": Article.AUDIENCE_RESIDENT,
        "related_priority": Article.PRIORITY_EMERGENCY,
        "summary": "Call 0800 111 999. Open windows. Do not use switches if the smell is strong.",
        "body": """Call the National Gas Emergency Service on 0800 111 999. This is not the same as the repairs line.

Open windows and doors. Do not smoke. Do not use matches. If the smell is strong, avoid light switches and the doorbell.

If you know where the gas meter is and can reach it safely, turn it off. If you cannot find it, wait for the emergency service.

Tell the housing advisor afterwards so they can record that the emergency service was called. A heating engineer should only be booked once the supply is safe.""",
    },
    {
        "category": "call-handling",
        "title": "Finding the stopcock on the call",
        "slug": "finding-the-stopcock",
        "audience": Article.AUDIENCE_ADVISOR,
        "related_priority": Article.PRIORITY_MIXED,
        "summary": "Ask the resident to look, do not tell them to force a seized valve, and write the result on the works order.",
        "body": """On an active leak, ask whether they can find the stopcock. Typical places: under the kitchen sink, in a downstairs cupboard, by the front door, or where the supply enters the property. In flats it may be in a communal cupboard — do not send them into a locked riser.

If they find it, ask them to turn it clockwise to stop the water, then confirm whether the leak has slowed. Record: found / not found / seized / turned.

If it will not move, tell them to stop. A seized stopcock is a job for the plumber, not a resident with a wrench.

Put the result on the works order. A plumber who knows the water is already off brings a different kit from one attending a flood.""",
    },
    {
        "category": "water-leak",
        "title": "Water leak — advisor questions and priority",
        "slug": "water-leak-advisor-priority",
        "audience": Article.AUDIENCE_ADVISOR,
        "related_priority": Article.PRIORITY_MIXED,
        "summary": "What to ask, when it is Emergency, and how to brief the plumber. Matches the diagnostic-tool rules.",
        "body": """Ask, in order: Is water still coming through? Can they contain it with a bowl or the stopcock? Has water reached sockets, lights, a consumer unit or a fused spur? Is a neighbour affected?

Water on electrics: Emergency, Plumber / Electrician, attend in hours. Tell the resident not to use those fittings.

Active leak that cannot be contained: Emergency, Plumber.

Active leak that is contained: Urgent, Plumber (not Routine). The water is still running.

No current leak, only a stain or a historic drip: Routine investigation, 28 days, still with a plumber.

On the works order record: room, whether the stopcock was used, neighbour affected, and electrical risk. That is what the contractor reads on arrival.

See also: Finding the stopcock, and Who to send.""",
    },
    {
        "category": "water-leak",
        "title": "Resident: what to do while waiting for a leak",
        "slug": "resident-waiting-for-a-leak",
        "audience": Article.AUDIENCE_RESIDENT,
        "related_priority": Article.PRIORITY_EMERGENCY,
        "summary": "Stopcock, bowls, electrics, and what not to do before the plumber arrives.",
        "body": """If water is still running, try the stopcock under the kitchen sink or where the supply enters the property. Turn it clockwise. If it will not move, stop — do not force it.

Catch water with a bowl and empty it. Move furniture and plugs away from the drip. Do not use sockets or lights that have got wet.

If water is near the fuse box or sockets, stay away from those fittings and tell the advisor so an electrician can attend with the plumber.

Photograph the leak and the ceiling or floor. That helps the contractor see whether it has spread since you reported it.""",
    },
    {
        "category": "electrical",
        "title": "Electrical hazards — sparking, burning smell, power loss",
        "slug": "electrical-hazards-advisor",
        "audience": Article.AUDIENCE_ADVISOR,
        "related_priority": Article.PRIORITY_EMERGENCY,
        "summary": "Sparking or a burning smell is Emergency. Power loss still needs a clear record.",
        "body": """Sparking, a burning smell, scorched fittings or a hot socket is Emergency for an electrician. Do not book this as a routine inspection.

Ask whether they can smell burning now, whether a breaker keeps tripping, and whether the whole property or one circuit is out.

Advise them not to reset a breaker that has already tripped more than once, and not to use the affected fitting.

Complete power loss with no burning is Urgent. Record which rooms are dark and whether the neighbour still has power — that tells the electrician if it is a landlord supply or a network issue.

Never tell a resident to remove a faceplate or tighten a live connection.""",
    },
    {
        "category": "electrical",
        "title": "Resident: unsafe electrics and power cuts",
        "slug": "resident-unsafe-electrics",
        "audience": Article.AUDIENCE_RESIDENT,
        "related_priority": Article.PRIORITY_EMERGENCY,
        "summary": "Do not use a fitting that sparks or smells of burning. One reset only if a breaker has tripped.",
        "body": """If a socket, switch or light is sparking, hot, or smells of burning, stop using it. If you can do so safely, switch that circuit off at the fuse box. Do not take the faceplate off.

If a breaker keeps tripping, do not keep resetting it. Tell the advisor which rooms went dark.

Check whether a neighbour still has power. If the whole street is out, it may be the network, not a housing repair — still tell the advisor so they can record it.

Use a torch rather than candles if the lights are out, especially if there is also a gas smell.""",
    },
    {
        "category": "heating",
        "title": "No heating or hot water — vulnerability changes the SLA",
        "slug": "heating-failure-vulnerability",
        "audience": Article.AUDIENCE_ADVISOR,
        "related_priority": Article.PRIORITY_MIXED,
        "summary": "Heating failure plus a vulnerable resident is Emergency. Capture who is in the household.",
        "body": """Ask: Is the heating off? Is there still hot water? Who lives there (child, older person, someone whose health is made worse by cold)?

No heating and a vulnerable resident: Emergency, Heating Engineer.

No heating, or no hot water, without that vulnerability: Urgent, Heating Engineer. Do not default to Routine 28 days because the boiler is 'just old'.

Record the boiler make if known, any fault code, and whether they have tried the reset once. One reset is enough to ask about.

If there is a smell of gas, this is not a heating-engineer diary job. Use the gas emergency article and 0800 111 999 first.""",
    },
    {
        "category": "heating",
        "title": "Resident: no heating or hot water",
        "slug": "resident-no-heating",
        "audience": Article.AUDIENCE_RESIDENT,
        "related_priority": Article.PRIORITY_URGENT,
        "summary": "One reset only. Say who lives in the home. Smell of gas is a different number.",
        "body": """If the boiler has a reset button, you can try it once. If it fails again, leave it off and tell the advisor the fault code if there is one on the display.

Say if children, an older person, or someone who is unwell lives there. That changes how quickly an engineer should attend.

Use extra bedding and, if it is safe, a room that still has some heat. Do not use outdoor heaters indoors.

If you can smell gas, stop and call 0800 111 999. Do not keep resetting the boiler.""",
    },
    {
        "category": "damp-and-mould",
        "title": "Damp and mould — children under 5 and respiratory risk",
        "slug": "damp-mould-urgent-risk",
        "audience": Article.AUDIENCE_ADVISOR,
        "related_priority": Article.PRIORITY_URGENT,
        "summary": "Visible mould with a child under 5, a respiratory condition, or an issue over 28 days is Urgent.",
        "body": """Do not close damp and mould as 'lifestyle' on the first call. Ask whether mould is visible, how long it has been there, whether anyone is under 5, and whether anyone has asthma or another respiratory condition.

Visible mould plus a child under 5, a respiratory condition, or more than 28 days: Urgent (7 days), Damp Specialist. That is a works order and a case record, not wipe-and-wait.

Capture room, wall or ceiling, size of the patch, and any leak. Photos help the surveyor; do not delay the job if they cannot send one.

If there is an active leak behind the mould, raise the leak as well so the specialist is not sent to a still-wet defect.

Record what you told the resident. Later users need to see why it was Urgent rather than Routine.""",
    },
    {
        "category": "damp-and-mould",
        "title": "Resident: living with mould until the inspection",
        "slug": "resident-living-with-mould",
        "audience": Article.AUDIENCE_RESIDENT,
        "related_priority": Article.PRIORITY_URGENT,
        "summary": "Wipe if you can, ventilate, and do not paint over active mould.",
        "body": """You can wipe small patches with a mould cleaner if it is safe for you to do so, then dry the surface. Do not paint over mould — the inspection needs to see it.

Open windows when you can, and keep furniture slightly off cold external walls. This does not replace a repair if the mould keeps coming back.

Tell the advisor if a child under 5 lives there, or if anyone has a chest condition. That changes how quickly someone should attend.

If the mould is spreading quickly, or you can see water coming through, report it as a leak as well as damp.""",
    },
    {
        "category": "roofing",
        "title": "Roof leak or structural concern",
        "slug": "roofing-water-ingress",
        "audience": Article.AUDIENCE_ADVISOR,
        "related_priority": Article.PRIORITY_MIXED,
        "summary": "Water entering the property, or a structural concern, is not a 28-day inspection by default.",
        "body": """Ask whether water is entering now, whether ceilings are bowing or debris is falling, and whether loft or top-floor electrics are wet.

Water in and wet electrics: Emergency, Roofer, and flag electrical risk.

Water entering with dry electrics, or structural concern (loose structure, sagging, falling debris): Urgent, Roofer.

A historic stain with no current ingress: Routine, but log the room and when it last ran so the roofer is not sent on a dry day with no information.

Do not send a resident onto the roof. Loose tiles in the garden are a safety note for the path and for the contractor.""",
    },
    {
        "category": "roofing",
        "title": "Resident: water coming through the roof",
        "slug": "resident-roof-leak",
        "audience": Article.AUDIENCE_RESIDENT,
        "related_priority": Article.PRIORITY_URGENT,
        "summary": "Catch the water. Stay off the roof. Say if the loft electrics are wet.",
        "body": """Put a bowl under the drip and move beds or sofas away from a stained ceiling. If the ceiling is bulging, stay out of that room and tell the advisor.

Do not go onto the roof or into a wet loft to investigate.

If lights or sockets on the top floor have got wet, do not use them. Say so on the call so an electrician risk can be flagged with the roofer.

Photograph the stain and the water. That shows whether it has spread before the visit.""",
    },
    {
        "category": "doors-and-windows",
        "title": "Insecure door or window — security risk",
        "slug": "insecure-door-window",
        "audience": Article.AUDIENCE_ADVISOR,
        "related_priority": Article.PRIORITY_URGENT,
        "summary": "If the door cannot be secured or the window cannot be closed, do not book Routine.",
        "body": """Ask: Can the door be locked and left secure? Can the window be closed? Are they at home tonight? Has there already been a break-in?

Security compromised (broken lock after burglary, communal door on the latch, property cannot be left): Emergency, Locksmith.

Door that cannot be secured: Urgent, Locksmith.

Window that cannot be closed: Urgent, Joiner.

Split locksmith and joiner if both are needed. Record whether a make-safe, boarding or temporary lock is enough until a full replacement.""",
    },
    {
        "category": "doors-and-windows",
        "title": "Resident: door or window that will not lock",
        "slug": "resident-insecure-door-window",
        "audience": Article.AUDIENCE_RESIDENT,
        "related_priority": Article.PRIORITY_URGENT,
        "summary": "Say if you cannot lock up tonight. Do not leave a door on the latch without telling the advisor.",
        "body": """If the door will not lock, or a window will not close, tell the advisor whether you can stay in the property tonight.

Do not leave the door on the latch and go out. If you have to leave, say so — that is a security risk, not a routine joinery job.

You can use a spare room if one window is stuck, as long as the front door still locks.

If glass is broken, keep people and pets away from it. Do not board it yourself unless you already have a safe way to do so; the contractor can make it safe.""",
    },
    {
        "category": "electrical",
        "title": "Communal lighting on the estate",
        "slug": "communal-lighting",
        "audience": Article.AUDIENCE_ADVISOR,
        "related_priority": Article.PRIORITY_ROUTINE,
        "summary": "Dark communal lights are usually Routine unless they leave a staircase unsafe.",
        "body": """Ask which block, which floor, and whether the stairs or a fire route are in darkness.

A single lamp out on a landing is Routine, electrician. A whole staircase or exit route in darkness is Urgent because people cannot leave safely.

Record the landlord lighting board location if the resident knows it. Do not send them into a locked riser.

This article is seeded with an overdue review date so document control can be demonstrated.""",
        "reviewed_on": date(2024, 9, 1),
        "reviewed_by": "Neighbourhood Officer",
    },
    {
        "category": "call-handling",
        "title": "Out-of-hours contractor briefing — draft",
        "slug": "out-of-hours-briefing-draft",
        "audience": Article.AUDIENCE_ADVISOR,
        "related_priority": Article.PRIORITY_EMERGENCY,
        "summary": "Draft script for what to tell the out-of-hours contractor. Not yet reviewed.",
        "body": """This is an unpublished draft. Advisors should not see it until a coordinator has reviewed it against the current out-of-hours contract.

Intended content: what to read out (address, access, vulnerability, electrical risk) and what not to promise on attendance time.

Keep it unpublished until reviewed_on and reviewed_by are set.""",
        "published": False,
        "reviewed_on": None,
        "reviewed_by": "",
    },
]


class Command(BaseCommand):
    help = "Load demo advisor user and starter knowledge articles."

    def handle(self, *args, **options):
        user, created = User.objects.get_or_create(
            username="advisor",
            defaults={"is_staff": False, "is_superuser": False},
        )
        user.set_password("changeme")
        user.save()
        self.stdout.write("Demo user advisor / changeme " + ("created" if created else "updated"))

        admin, admin_created = User.objects.get_or_create(
            username="admin",
            defaults={"is_staff": True, "is_superuser": True},
        )
        admin.set_password("changeme")
        admin.is_staff = True
        admin.is_superuser = True
        admin.save()
        self.stdout.write("Admin user admin / changeme " + ("created" if admin_created else "updated"))

        for data in CATEGORIES:
            Category.objects.update_or_create(slug=data["slug"], defaults=data)
        self.stdout.write(f"{len(CATEGORIES)} categories loaded")

        for data in ARTICLES:
            category = Category.objects.get(slug=data["category"])
            payload = {k: v for k, v in data.items() if k != "category"}
            payload["category"] = category
            payload.setdefault("published", True)
            if payload["published"]:
                payload.setdefault("reviewed_on", DEFAULT_REVIEWED_ON)
                payload.setdefault("reviewed_by", DEFAULT_REVIEWED_BY)
            Article.objects.update_or_create(slug=data["slug"], defaults=payload)
        self.stdout.write(f"{len(ARTICLES)} articles loaded")
