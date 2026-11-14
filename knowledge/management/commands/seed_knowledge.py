from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from knowledge.models import Article, Category

CATEGORIES = [
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
        "category": "water-leak",
        "title": "Water leak — advisor questions and priority",
        "slug": "water-leak-advisor-priority",
        "audience": Article.AUDIENCE_ADVISOR,
        "related_priority": Article.PRIORITY_MIXED,
        "summary": "What to ask, when it is Emergency, and how to brief the plumber.",
        "body": """This article is for advisors logging a leak. It matches the diagnostic-tool rules: active leak, whether it is contained, and whether electrics are affected.

Ask, in order: Is water still coming through? Can the resident contain it with a bowl or by turning a stopcock? Has water reached sockets, lights, a consumer unit, or a fused spur?

If water is on electrics, treat as Emergency and send Plumber / Electrician. Do not tell the resident to keep using those fittings. Advise them to avoid the wet fittings and, if they can do so safely, switch off at the consumer unit.

An uncontained leak (still running, flooding a room, or entering a neighbour) is Emergency even if electrics are dry. A contained drip with no electrical risk is usually Routine inspection, unless the resident is vulnerable and cannot manage the water.

On the works order record: location (kitchen, bathroom, ceiling), whether the stopcock was used, and whether a neighbour is affected. That is what the contractor reads on arrival.""",
    },
    {
        "category": "water-leak",
        "title": "Resident: what to do while waiting for a leak",
        "slug": "resident-waiting-for-a-leak",
        "audience": Article.AUDIENCE_RESIDENT,
        "related_priority": Article.PRIORITY_EMERGENCY,
        "summary": "Stopcock, bowls, electrics, and what not to do before the plumber arrives.",
        "body": """If water is still running, try the stopcock under the kitchen sink or where the supply enters the property. If you cannot find it, do not force valves.

Catch water with a bowl and empty it. Move furniture and electrics away from the drip. Do not use sockets or lights that have got wet.

If water is near the fuse box or sockets, stay away from those fittings and tell the advisor so an electrician can attend with the plumber.

Photograph the leak and the ceiling or floor it is coming through. That helps the contractor see whether the leak has spread since you reported it.""",
    },
    {
        "category": "electrical",
        "title": "Electrical hazards — sparking, burning smell, power loss",
        "slug": "electrical-hazards-advisor",
        "audience": Article.AUDIENCE_ADVISOR,
        "related_priority": Article.PRIORITY_EMERGENCY,
        "summary": "Sparking or a burning smell is Emergency. Power loss still needs a clear record.",
        "body": """Sparking, a burning smell, scorched fittings or a hot socket is Emergency for an electrician. Do not book this as a routine inspection.

Ask whether the resident can smell burning now, whether a breaker keeps tripping, and whether the whole property or one circuit is out.

Advise the resident not to reset a breaker that has already tripped more than once, and not to use the affected fitting.

Power loss with no burning or sparking may still be Urgent if the resident is vulnerable (no lighting, no heating controls, or they cannot leave the property safely). Record which rooms are dark and whether the neighbour still has power — that helps the electrician decide if it is a landlord supply or a network issue.

Never tell a resident to remove a faceplate or tighten a live connection.""",
    },
    {
        "category": "heating",
        "title": "No heating or hot water — vulnerability changes the SLA",
        "slug": "heating-failure-vulnerability",
        "audience": Article.AUDIENCE_ADVISOR,
        "related_priority": Article.PRIORITY_MIXED,
        "summary": "Heating failure plus a vulnerable resident is Emergency. Capture who is in the household.",
        "body": """Ask: Is the heating off? Is there still hot water? Who lives there (children, older person, someone with a health condition that is made worse by cold)?

Heating failure with a vulnerable resident is Emergency for a heating engineer. Heating failure with no vulnerability is still usually Urgent in cold weather — do not default to Routine 28 days because the boiler is 'just old'.

Record the boiler make if known, any fault code on the display, and whether the resident has tried the reset once. One reset is enough to ask about; repeated resets can hide an unsafe appliance.

If there is a smell of gas, this is not a heating-engineer diary job. Direct the resident to the gas emergency number and log that you did so. Do not send a routine heating job in parallel until the supply is declared safe.""",
    },
    {
        "category": "damp-and-mould",
        "title": "Damp and mould — children under 5 and respiratory risk",
        "slug": "damp-mould-urgent-risk",
        "audience": Article.AUDIENCE_ADVISOR,
        "related_priority": Article.PRIORITY_URGENT,
        "summary": "Visible mould with a child under 5, a respiratory condition, or an issue over 28 days is Urgent.",
        "body": """Do not close damp and mould as 'lifestyle' on the first call. Ask whether mould is visible, how long it has been present, whether anyone in the household is under 5, and whether anyone has asthma or another respiratory condition.

Visible mould plus a child under 5, a respiratory condition, or an issue lasting more than 28 days maps to Urgent (7 days) in the diagnostic rules. Treat that as a works order and a case record, not advice to wipe and wait.

Capture room, wall or ceiling, size of the patch, and any leak or cold-bridge the resident has already noticed. Photograph requests help the surveyor, but do not delay the job if the resident cannot send a photo.

If there is an active leak behind the mould, raise the leak as well so the damp specialist is not sent to a still-wet defect.

Advisors should record what they told the resident. Later users (housing officer, surveyor, contractor) need to see why the job was Urgent rather than Routine.""",
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

If the mould is spreading quickly, or you can see water coming through, report it again as a leak as well as damp.""",
    },
    {
        "category": "roofing",
        "title": "Roof leak or structural concern",
        "slug": "roofing-water-ingress",
        "audience": Article.AUDIENCE_ADVISOR,
        "related_priority": Article.PRIORITY_MIXED,
        "summary": "Water entering the property or a structural concern is not a 28-day inspection by default.",
        "body": """Ask whether water is entering the property now, whether ceilings are bowing or debris is falling, and whether electrics in the loft or top floor are wet.

Water entering the property, or any sign of structural movement, is Emergency or Urgent depending on how fast it is progressing. Wet electrics in the loft follow the same rule as any other leak: Emergency, and flag electrical risk on the order.

A historic stain with no current ingress can be Routine, but still log the room and when it last ran so the roofer is not sent on a dry day with no information.

Do not send a resident onto the roof. If they mention loose tiles in the garden, treat that as a safety note for the contractor and for anyone using the path.""",
    },
    {
        "category": "doors-and-windows",
        "title": "Insecure door or window — security risk",
        "slug": "insecure-door-window",
        "audience": Article.AUDIENCE_ADVISOR,
        "related_priority": Article.PRIORITY_URGENT,
        "summary": "If the door cannot be secured or the window cannot be closed, do not book Routine.",
        "body": """Ask: Can the door be locked and left secure? Can the window be closed? Is the resident at home tonight? Has there already been an attempted break-in?

A door that cannot be secured, or a window that cannot be closed, is Urgent. A security risk (broken lock after a burglary, or a communal door on the latch) is Emergency.

Trade is usually locksmith for locks and ironmongery, joiner for frames and glass. Split the order if both are needed rather than sending the wrong trade twice.

Record whether a temporary lock, boarding, or a make-safe is enough until a full replacement. That is what the contractor needs to bring.""",
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
            payload["published"] = True
            Article.objects.update_or_create(slug=data["slug"], defaults=payload)
        self.stdout.write(f"{len(ARTICLES)} articles loaded")
