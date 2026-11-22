---
{
  "slug": "culverizer",
  "dates": "April 2022 - Present",
  "template": "combat-robot",
  "gallery": [
    {"file": "competition.png", "caption": "Culverizer v3 in competition at Open Sauce 2023"},
    {"file": "culverizer-vs-hound.jpg", "caption": "Culverizer vs Hound at Motown Bot Showdown (April 2026)"},
    {"file": "culverizer-configurations.jpg", "caption": "Culverizer (vert config) and Culverizer (hammersaw config)"},
    {"file": "culverizer-arm-machining.png", "caption": "Aluminum arm blank in Haas VF4 for machining"}
  ],
  "section_images": {
    "Competition Results": {"file": "culverizer-competition-results.jpg", "caption": "Culverizer beside its third-place award at Midwest Robot Rumble."},
    "Weapon Assembly": {"file": "weapon-cross-section-cutout.png", "caption": "Cross-section of the weapon assembly.", "additional": [{"file": "weapon-spline-cutout.png", "caption": "Blade spline pattern."}]},
    "Drivetrain": {"file": "culverizer-drivetrain-cutout.png", "match_text_height": true, "caption": "Culverizer drive assembly with a brushless motor, custom urethane wheel, and spring-steel cleats."},
    "Design approach": {"file": "culverizer-design-approach-cutout.png", "match_text_height": true, "caption": "Top-view CAD assembly of Culverizer showing the weapon, chassis, wheels, and armor."}
  },
  "section_links": {"Competition Results": {"label": "Watch Culverizer in action ↗", "url": "https://www.youtube.com/watch?v=33ErYOWSm2E"}},
  "robot": {
    "type": "Horizontal spinner",
    "weight": "3 lb / Beetleweight",
    "record": "18-15",
    "competitions": "7 tournaments",
    "energy": "700 J",
    "version": "v4.2",
    "wins": 18,
    "losses": 15
  },
  "title": "Culverizer",
  "category": "Combat robotics",
  "subtitle": "A 3 lb horizontal-spinner combat robot",
  "role": "Lead Engineer: design, manufacturing, electronics, & testing\nCompetition strategy and drive coach",
  "summary": "A compact combat robot built around a heavy horizontal blade, a rigid carbon-fiber chassis, and impact-absorbing TPU armor.",
  "metrics": [
    [
      "3 lb",
      "weight class"
    ],
    [
      "18-15",
      "v4.2 match record"
    ],
    [
      "7",
      "v4.2 tournaments"
    ]
  ],
  "tags": [
    "Solid mechanics",
    "Dynamic FEA",
    "Additive manufacturing",
    "CNC machining"
  ],
  "images": [
    {
      "file": "culverizer-photo-cutout.png",
      "caption": "Culverizer with its background removed, showing the chassis, weapon, and attached safety tag.",
      "show_caption": false
    },
    {
      "file": "culverizer.png",
      "caption": "Culverizer CAD assembly: carbon-fiber plates and a compliant TPU body."
    },
    {
      "file": "weapon.png",
      "caption": "Weapon assembly section showing the pulley, shoulder bolt, and bearing arrangement."
    },
    {
      "file": "competition.png",
      "caption": "Culverizer in competition, from the original portfolio."
    }
  ],
  "source": "Manan Singh Mechanical Portfolio.pptx, slides 2–7; v4.2 updates from Manan, November 2, 2026",
  "review_status": "v4.2 role, record, tournament count, and energy confirmed by Manan on November 2, 2026. Other design details retain historical source context.",
  "show_review_note": false
}
---
## Design approach
I designed Culverizer around an offense-first strategy, using a heavy, hardened steel blade to destroy opponents' wheels and batter their weapon assemblies.

Carbon-fiber plates provide chassis rigidity and support the weapon assembly, while the 3D-printed 95A TPU body flexes to absorb and disperse impact energy. The TPU serves as sacrificial armor, taking damage to protect the internal electronics.

## Drivetrain
Brushless motors propel Culverizer at 12 mph. TPU shock mounts let the motors deflect under impact, directing energy away from the gearboxes to extend their lifespan.

I made custom molds for 2.1-inch wheels with impact-absorbing TPU cores and 45A urethane treads. The urethane adheres to the TPU and provides traction and acceleration; 1/32-inch spring-steel "spiked cleats" further improve traction and control. The compliant cores also help protect the wheels and gearmotors from impact.

## Weapon Assembly
A 600 kV motor at 25.2 V drives the blade through a 6:5 belt reduction, reaching a measured 220 mph and storing 700 J of energy. The flat timing belt allows the assembly to slip on impact, reducing shock transferred to the motor. A spline pattern transfers torque to the blade.

## Competition Results
I built three working copies of Culverizer, configured to counter different opponent build styles. Across seven competitions, v4.2 earned an 18-15 record (54.5% win rate), including two third-place finishes.
