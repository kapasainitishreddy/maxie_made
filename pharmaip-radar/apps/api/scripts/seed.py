"""Seed the database with realistic sample pharma patents."""

from __future__ import annotations

import asyncio
import uuid
from datetime import date

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import AsyncSessionLocal, engine, Base
from app.models.org import Org, OrgRole, OrgMember
from app.models.patent import Patent, PatentClaim, PatentStatus
from app.models.user import User


SAMPLE_PATENTS = [
    {
        "patent_number": "US11234856B2",
        "jurisdiction": "US",
        "title": "Anti-PD-1 antibodies and uses thereof",
        "abstract": "The present invention provides isolated monoclonal antibodies that specifically bind to PD-1 and block the interaction between PD-1 and its ligands PD-L1 and PD-L2.",
        "assignee": "Merck Sharp & Dohme Corp.",
        "drug_name": "Keytruda (pembrolizumab)",
        "therapeutic_area": "Oncology",
        "inventors": ["Caroline E. Jonas", "David A. Berman"],
        "ipc_classes": ["C07K16/28", "A61K39/395"],
        "filing_date": date(2018, 6, 12),
        "grant_date": date(2022, 3, 1),
        "expiration_date": date(2038, 6, 12),
        "claims": [
            "An isolated monoclonal antibody that binds PD-1, comprising a heavy chain CDR3 sequence; wherein the antibody blocks PD-1 binding to PD-L1; and wherein the antibody is humanized.",
            "A pharmaceutical composition comprising the antibody of claim 1; and a pharmaceutically acceptable carrier.",
        ],
    },
    {
        "patent_number": "US11236500B2",
        "jurisdiction": "US",
        "title": "IL-23 antagonists and methods of use",
        "abstract": "Antibodies that bind IL-23 and methods of using the antibodies to treat inflammatory and autoimmune disorders.",
        "assignee": "AbbVie Inc.",
        "drug_name": "Skyrizi (risankizumab)",
        "therapeutic_area": "Immunology",
        "inventors": ["Anne M. Fourie", "Rolf E. Swenson"],
        "ipc_classes": ["C07K16/24", "A61P37/00"],
        "filing_date": date(2016, 8, 4),
        "grant_date": date(2022, 1, 18),
        "expiration_date": date(2036, 8, 4),
        "claims": [
            "An anti-IL-23 antibody comprising a heavy chain variable region; a light chain variable region; wherein the antibody binds human IL-23 with KD < 100pM.",
        ],
    },
    {
        "patent_number": "US10590153B2",
        "jurisdiction": "US",
        "title": "Compositions comprising adalimumab",
        "abstract": "Stable aqueous pharmaceutical compositions comprising adalimumab for subcutaneous injection.",
        "assignee": "AbbVie Inc.",
        "drug_name": "Humira (adalimumab)",
        "therapeutic_area": "Immunology",
        "inventors": ["Alavattam Sreedhara", "Rolf E. Swenson"],
        "ipc_classes": ["A61K39/395", "C07K16/24"],
        "filing_date": date(2014, 5, 2),
        "grant_date": date(2020, 3, 17),
        "expiration_date": date(2034, 5, 2),
        "claims": [
            "A pharmaceutical composition comprising adalimumab; citrate buffer; polysorbate 80; wherein the composition is stable at 2-8°C for at least 24 months.",
        ],
    },
    {
        "patent_number": "US10730908B2",
        "jurisdiction": "US",
        "title": "Apixaban formulations and methods of treatment",
        "abstract": "Solid oral dosage forms comprising apixaban for the treatment and prevention of thromboembolic disorders.",
        "assignee": "Bristol-Myers Squibb Company",
        "drug_name": "Eliquis (apixaban)",
        "therapeutic_area": "Cardiology",
        "inventors": ["Chandra V. S. R. Prasad", "Donald J. T. M."],
        "ipc_classes": ["A61K31/437", "C07D471/04"],
        "filing_date": date(2015, 3, 9),
        "grant_date": date(2020, 7, 28),
        "expiration_date": date(2031, 11, 21),
        "claims": [
            "An oral pharmaceutical composition comprising apixaban; lactose monohydrate; microcrystalline cellulose; croscarmellose sodium; magnesium stearate.",
        ],
    },
    {
        "patent_number": "US11026959B2",
        "jurisdiction": "US",
        "title": "Aflibercept formulations for intravitreal injection",
        "abstract": "Pharmaceutical compositions comprising aflibercept for the treatment of ocular disorders.",
        "assignee": "Regeneron Pharmaceuticals Inc.",
        "drug_name": "Eylea (aflibercept)",
        "therapeutic_area": "Ophthalmology",
        "inventors": ["Daniel R. W."],
        "ipc_classes": ["A61K38/17", "C07K14/71"],
        "filing_date": date(2013, 9, 10),
        "grant_date": date(2021, 6, 8),
        "expiration_date": date(2033, 9, 10),
        "claims": [
            "A method of treating neovascular age-related macular degeneration comprising intravitreally administering aflibercept; at a dose of 2mg every 4 weeks.",
        ],
    },
    {
        "patent_number": "US11034725B2",
        "jurisdiction": "US",
        "title": "CAR-T cell therapy targeting CD19",
        "abstract": "Chimeric antigen receptor T cells targeting CD19 for the treatment of B-cell malignancies.",
        "assignee": "Novartis AG",
        "drug_name": "Kymriah (tisagenlecleucel)",
        "therapeutic_area": "Oncology",
        "inventors": ["Stephan A. Grupp"],
        "ipc_classes": ["C12N5/0783", "A61K35/17"],
        "filing_date": date(2014, 11, 12),
        "grant_date": date(2021, 6, 22),
        "expiration_date": date(2034, 11, 12),
        "claims": [
            "A chimeric antigen receptor (CAR) comprising an anti-CD19 scFv; a CD3-zeta signaling domain; a CD137 costimulatory domain.",
        ],
    },
    {
        "patent_number": "US11542308B2",
        "jurisdiction": "US",
        "title": "mRNA vaccines for infectious diseases",
        "abstract": "Lipid nanoparticle-encapsulated mRNA vaccines encoding antigenic proteins.",
        "assignee": "ModernaTX Inc.",
        "drug_name": "Spikevax (mRNA-1273)",
        "therapeutic_area": "Infectious Disease",
        "inventors": ["Derrick J. H. R."],
        "ipc_classes": ["A61K9/127", "C12N15/88"],
        "filing_date": date(2020, 1, 11),
        "grant_date": date(2023, 1, 3),
        "expiration_date": date(2040, 1, 11),
        "claims": [
            "A lipid nanoparticle comprising an mRNA encoding a SARS-CoV-2 spike protein; wherein the mRNA is modified with N1-methylpseudouridine.",
        ],
    },
    {
        "patent_number": "US11111270B2",
        "jurisdiction": "US",
        "title": "GLP-1 receptor agonist semaglutide formulations",
        "abstract": "Pharmaceutical compositions comprising semaglutide for the treatment of type 2 diabetes.",
        "assignee": "Novo Nordisk A/S",
        "drug_name": "Ozempic (semaglutide)",
        "therapeutic_area": "Endocrinology",
        "inventors": ["Lars H. E. B."],
        "ipc_classes": ["A61K38/26", "C07K14/605"],
        "filing_date": date(2012, 10, 26),
        "grant_date": date(2021, 9, 7),
        "expiration_date": date(2032, 10, 26),
        "claims": [
            "A pharmaceutical composition comprising semaglutide; propylene glycol; phenol; zinc; wherein the composition is for subcutaneous injection.",
        ],
    },
    {
        "patent_number": "US11015000B2",
        "jurisdiction": "US",
        "title": "BTK inhibitor ibrutinib for hematologic malignancies",
        "abstract": "Covalent inhibitors of Bruton's tyrosine kinase and uses thereof.",
        "assignee": "Pharmacyclics LLC",
        "drug_name": "Imbruvica (ibrutinib)",
        "therapeutic_area": "Hematology",
        "inventors": ["Wei C. C."],
        "ipc_classes": ["C07D487/04", "A61K31/519"],
        "filing_date": date(2011, 7, 27),
        "grant_date": date(2021, 5, 25),
        "expiration_date": date(2031, 7, 27),
        "claims": [
            "A compound of formula I; wherein the compound inhibits BTK with IC50 < 100nM; and wherein R1 is a phenoxyphenyl group.",
        ],
    },
    {
        "patent_number": "US11129888B2",
        "jurisdiction": "US",
        "title": "Duchenne muscular dystrophy antisense oligonucleotides",
        "abstract": "Antisense oligonucleotides for the treatment of Duchenne muscular dystrophy by exon skipping.",
        "assignee": "Sarepta Therapeutics Inc.",
        "drug_name": "Exondys 51 (eteplirsen)",
        "therapeutic_area": "Rare Disease",
        "inventors": ["Stephen D. W."],
        "ipc_classes": ["C12N15/113", "A61K31/7088"],
        "filing_date": date(2009, 12, 18),
        "grant_date": date(2021, 9, 28),
        "expiration_date": date(2029, 12, 18),
        "claims": [
            "An antisense oligonucleotide of SEQ ID NO: 1; a morpholino backbone; for use in skipping exon 51 of the human dystrophin gene.",
        ],
    },
    {
        "patent_number": "US11246843B2",
        "jurisdiction": "US",
        "title": "Anti-CD20 antibody obinutuzumab",
        "abstract": "Glycoengineered type II anti-CD20 antibodies for the treatment of B-cell lymphomas.",
        "assignee": "Genentech Inc.",
        "drug_name": "Gazyva (obinutuzumab)",
        "therapeutic_area": "Oncology",
        "inventors": ["Pablo U. S."],
        "ipc_classes": ["C07K16/28", "A61P35/00"],
        "filing_date": date(2010, 4, 8),
        "grant_date": date(2022, 2, 22),
        "expiration_date": date(2030, 4, 8),
        "claims": [
            "A glycoengineered anti-CD20 antibody; wherein the antibody has increased ADCC compared to rituximab; a non-fucosylated Fc region.",
        ],
    },
    {
        "patent_number": "EP3452500B1",
        "jurisdiction": "EP",
        "title": "Tagrisso (osimertinib) formulations",
        "abstract": "Third-generation EGFR inhibitors for the treatment of non-small cell lung cancer.",
        "assignee": "AstraZeneca AB",
        "drug_name": "Tagrisso (osimertinib)",
        "therapeutic_area": "Oncology",
        "inventors": ["Richard A. W."],
        "ipc_classes": ["C07D403/12", "A61K31/517"],
        "filing_date": date(2016, 5, 12),
        "grant_date": date(2021, 11, 17),
        "expiration_date": date(2036, 5, 12),
        "claims": [
            "A compound of formula II; an irreversible inhibitor of EGFR T790M; wherein R2 is a methoxy group.",
        ],
    },
    {
        "patent_number": "WO2021000001A1",
        "jurisdiction": "WO",
        "title": "CRISPR-Cas9 gene editing compositions",
        "abstract": "Compositions and methods for CRISPR-Cas9 mediated gene editing in vivo.",
        "assignee": "Editas Medicine Inc.",
        "drug_name": "EDIT-101",
        "therapeutic_area": "Rare Disease",
        "inventors": ["Morgan L. M."],
        "ipc_classes": ["C12N9/22", "C12N15/90"],
        "filing_date": date(2020, 7, 1),
        "grant_date": None,
        "expiration_date": date(2040, 7, 1),
        "claims": [
            "A composition comprising a guide RNA targeting the CEP290 gene; a Cas9 protein; a lipid nanoparticle; for use in treating Leber congenital amaurosis.",
        ],
    },
    {
        "patent_number": "US11396531B2",
        "jurisdiction": "US",
        "title": "Trikafta (elexacaftor/tezacaftor/ivacaftor) combination",
        "abstract": "Triple combination therapy for cystic fibrosis transmembrane conductance regulator modulators.",
        "assignee": "Vertex Pharmaceuticals Inc.",
        "drug_name": "Trikafta",
        "therapeutic_area": "Rare Disease",
        "inventors": ["Steven A. M."],
        "ipc_classes": ["A61K31/4704", "C07D215/22"],
        "filing_date": date(2017, 3, 9),
        "grant_date": date(2022, 7, 19),
        "expiration_date": date(2037, 3, 9),
        "claims": [
            "A pharmaceutical composition comprising elexacaftor; tezacaftor; ivacaftor; in a fixed-dose combination; for oral administration.",
        ],
    },
    {
        "patent_number": "US11278522B2",
        "jurisdiction": "US",
        "title": "Lemtrada (alemtuzumab) anti-CD52 antibody",
        "abstract": "Humanized monoclonal antibodies specific for CD52 for the treatment of multiple sclerosis.",
        "assignee": "Genzyme Corp.",
        "drug_name": "Lemtrada (alemtuzumab)",
        "therapeutic_area": "Neurology",
        "inventors": ["Geoff Hale"],
        "ipc_classes": ["C07K16/28", "A61K39/395"],
        "filing_date": date(2014, 12, 4),
        "grant_date": date(2022, 3, 15),
        "expiration_date": date(2034, 12, 4),
        "claims": [
            "A humanized anti-CD52 antibody; for use in treating relapsing-remitting multiple sclerosis; administered by intravenous infusion.",
        ],
    },
    {
        "patent_number": "US11103456B2",
        "jurisdiction": "US",
        "title": "Dupixent (dupilumab) anti-IL-4R antibody",
        "abstract": "Antibodies that bind IL-4 receptor alpha and inhibit signaling of both IL-4 and IL-13.",
        "assignee": "Regeneron Pharmaceuticals Inc.",
        "drug_name": "Dupixent (dupilumab)",
        "therapeutic_area": "Immunology",
        "inventors": ["Jamie M. O."],
        "ipc_classes": ["C07K16/28", "A61K39/395"],
        "filing_date": date(2012, 5, 7),
        "grant_date": date(2021, 8, 31),
        "expiration_date": date(2032, 5, 7),
        "claims": [
            "An antibody or antigen-binding fragment that binds IL-4Rα; blocks IL-4 and IL-13 signaling; a human IgG4 isotype.",
        ],
    },
    {
        "patent_number": "US11427800B2",
        "jurisdiction": "US",
        "title": "Tremfya (guselkumab) anti-IL-23 antibody",
        "abstract": "Human monoclonal antibodies specific for the p19 subunit of IL-23.",
        "assignee": "Janssen Biotech Inc.",
        "drug_name": "Tremfya (guselkumab)",
        "therapeutic_area": "Immunology",
        "inventors": ["Cynthia M. R."],
        "ipc_classes": ["C07K16/24", "A61P17/06"],
        "filing_date": date(2011, 12, 14),
        "grant_date": date(2022, 8, 30),
        "expiration_date": date(2031, 12, 14),
        "claims": [
            "A human anti-IL-23 antibody comprising heavy and light chain CDRs; wherein the antibody binds p19 subunit; a IgG1 isotype with reduced effector function.",
        ],
    },
    {
        "patent_number": "US11530222B2",
        "jurisdiction": "US",
        "title": "Vyndaqel (tafamidis) transthyretin stabilizer",
        "abstract": "Small molecule stabilizers of transthyretin for the treatment of transthyretin amyloid cardiomyopathy.",
        "assignee": "Pfizer Inc.",
        "drug_name": "Vyndaqel (tafamidis)",
        "therapeutic_area": "Rare Disease",
        "inventors": ["Jeffery W. K."],
        "ipc_classes": ["C07D263/32", "A61K31/421"],
        "filing_date": date(2013, 6, 6),
        "grant_date": date(2022, 12, 20),
        "expiration_date": date(2033, 6, 6),
        "claims": [
            "A compound of formula III; 2-(3,5-dichlorophenyl)-benzoxazole; for use in treating transthyretin amyloid cardiomyopathy.",
        ],
    },
    {
        "patent_number": "US11608700B2",
        "jurisdiction": "US",
        "title": "Entresto (sacubitril/valsartan) combination",
        "abstract": "Combination of a neprilysin inhibitor and an angiotensin II receptor blocker.",
        "assignee": "Novartis AG",
        "drug_name": "Entresto",
        "therapeutic_area": "Cardiology",
        "inventors": ["Kala S. B."],
        "ipc_classes": ["A61K31/41", "C07D257/04"],
        "filing_date": date(2010, 9, 1),
        "grant_date": date(2023, 3, 21),
        "expiration_date": date(2030, 9, 1),
        "claims": [
            "A pharmaceutical composition comprising sacubitril; valsartan; in a 1:1 molar ratio; as a sodium salt complex.",
        ],
    },
    {
        "patent_number": "US11720000B2",
        "jurisdiction": "US",
        "title": "Veklury (remdesivir) antiviral for COVID-19",
        "abstract": "Nucleoside prodrugs with broad-spectrum antiviral activity.",
        "assignee": "Gilead Sciences Inc.",
        "drug_name": "Veklury (remdesivir)",
        "therapeutic_area": "Infectious Disease",
        "inventors": ["Dustin B. S."],
        "ipc_classes": ["C07H19/10", "A61K31/675"],
        "filing_date": date(2017, 4, 13),
        "grant_date": date(2023, 6, 6),
        "expiration_date": date(2037, 4, 13),
        "claims": [
            "A compound of formula IV; an adenosine nucleotide analog prodrug; for use in treating RNA virus infections.",
        ],
    },
]


async def main() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSessionLocal() as db:
        # Check if already seeded
        existing = (await db.execute(select(Patent).limit(1))).scalar_one_or_none()
        if existing:
            print("Already seeded. Skipping.")
            return

        # Org + user
        org = Org(
            name="Demo Pharma Corp",
            slug="demo-pharma",
            clerk_org_id="org_demo_001",
            subscription_tier="pro",
        )
        db.add(org)
        await db.flush()

        user = User(
            clerk_id="user_demo_001",
            email="demo@pharmaip-radar.com",
            full_name="Demo User",
            default_org_id=org.id,
        )
        db.add(user)
        db.add(OrgMember(org_id=org.id, user_id=user.id, role=OrgRole.OWNER))

        # Patents + claims
        for p_data in SAMPLE_PATENTS:
            claims = p_data.pop("claims", [])
            patent = Patent(
                org_id=org.id,
                status=PatentStatus.GRANTED if p_data.get("grant_date") else PatentStatus.PENDING,
                **p_data,
            )
            db.add(patent)
            await db.flush()
            for i, ctext in enumerate(claims, 1):
                db.add(PatentClaim(
                    patent_id=patent.id,
                    claim_number=i,
                    claim_type="independent" if i == 1 else "dependent",
                    text=ctext,
                    is_independent=(i == 1),
                ))

        await db.commit()
        print(f"Seeded {len(SAMPLE_PATENTS)} patents.")


if __name__ == "__main__":
    asyncio.run(main())
