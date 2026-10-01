from fpdf import FPDF
import os


def export_comic_pdf(
    comic,
    output_path,
    comic_title="ComicCraft Comic"
):

    pdf = FPDF()

    pdf.set_auto_page_break(
        auto=True,
        margin=15
    )

    # Create output directory
    os.makedirs(
        os.path.dirname(output_path),
        exist_ok=True
    )

    # Title page
    pdf.add_page()

    pdf.set_font(
        "Arial",
        "B",
        24
    )

    pdf.cell(
        0,
        15,
        "COMICCRAFT",
        ln=True,
        align="C"
    )

    pdf.ln(10)

    pdf.set_font(
        "Arial",
        "B",
        18
    )

    pdf.multi_cell(
        0,
        10,
        comic_title,
        align="C"
    )

    pdf.ln(15)

    pdf.set_font(
        "Arial",
        "",
        12
    )

    pdf.multi_cell(
        0,
        8,
        "AI Generated Comic Story",
        align="C"
    )


    # Panel pages
    for panel in comic:

        pdf.add_page()

        # Panel number
        pdf.set_font(
            "Arial",
            "B",
            20
        )

        pdf.cell(
            0,
            12,
            f"Panel {panel['panel']}",
            ln=True
        )

        pdf.ln(5)


        # Panel title
        pdf.set_font(
            "Arial",
            "B",
            16
        )

        pdf.multi_cell(
            0,
            10,
            panel["title"]
        )

        pdf.ln(5)


        # Narration
        pdf.set_font(
            "Arial",
            "B",
            12
        )

        pdf.cell(
            0,
            8,
            "Narration:",
            ln=True
        )

        pdf.set_font(
            "Arial",
            "",
            12
        )

        pdf.multi_cell(
            0,
            8,
            panel["narration"]
        )

        pdf.ln(5)


        # Dialogue
        pdf.set_font(
            "Arial",
            "B",
            12
        )

        pdf.cell(
            0,
            8,
            "Dialogue:",
            ln=True
        )

        pdf.set_font(
            "Arial",
            "",
            12
        )

        pdf.multi_cell(
            0,
            8,
            panel["dialogue"]
        )

        pdf.ln(5)


        # Image description
        pdf.set_font(
            "Arial",
            "B",
            12
        )

        pdf.cell(
            0,
            8,
            "Visual Description:",
            ln=True
        )

        pdf.set_font(
            "Arial",
            "",
            11
        )

        pdf.multi_cell(
            0,
            7,
            panel["image_prompt"]
        )


    # Save PDF
    pdf.output(output_path)