import gradio as gr

from utils.data_loader import load_data
from utils.explanation import generate_explanation

from llm.openai_parser import parse_question

from pipeline import DataPipeline


# Load dataset once
df = load_data()

# Create pipeline once
pipeline = DataPipeline(df)


def chat(question):

    try:

        if not question.strip():

            return (
                {},
                "No question provided.",
                "Please enter a question.",
                {},
                None,
                0.0,
                "Needs Human Review"
            )

        query = parse_question(
            question
        )

        # Refusal Handling
        if query.get("intent") == "refuse":

            return (
                query,
                "The query cannot be answered from the available dataset.",
                query.get(
                    "reason",
                    "Question cannot be answered from dataset."
                ),
                {
                    "intent": "refuse"
                },
                None,
                0.0,
                "Needs Human Review"
            )

        result = pipeline.run(
            query
        )

        explanation = (
            generate_explanation(
                query
            )
        )

        return (
            query,
            explanation,
            result["answer"],
            result["provenance"],
            result.get(
                "chart_path"
            ),
            result.get(
                "confidence",
                1.0
            ),
            (
                "Needs Human Review"
                if result.get(
                    "needs_human_review",
                    False
                )
                else
                "Approved"
            )
        )

    except Exception as e:

        return (
            {
                "error": str(e)
            },
            "Pipeline execution failed.",
            str(e),
            {},
            None,
            0.0,
            "Needs Human Review"
        )


with gr.Blocks(
    title="Talk to Government Data"
) as demo:

    gr.Markdown(
        """
# Talk to Government Data

Ask questions about India's Air Quality dataset using natural language.

The system:
- Converts questions into structured JSON
- Executes real computations on the dataset
- Generates charts automatically
- Shows provenance
- Refuses out-of-scope questions
"""
    )

    with gr.Row():

        question_box = gr.Textbox(
            label="Ask a Question",
            placeholder="Example: Top 5 cities by PM2.5",
            lines=2,
            scale=8
        )

        ask_button = gr.Button(
            "Ask",
            scale=1
        )

    gr.Examples(
        examples=[
            ["Average PM2.5 in Bihar"],
            ["Maximum PM10 in Delhi"],
            ["Top 5 cities by PM2.5"],
            ["Bottom 10 stations by PM10"],
            ["Summarize PM2.5 in Delhi"],
            ["Show distribution of PM2.5"],
            ["Which states exist?"],
            ["Show Anand Vihar station"],
            ["Who is the Prime Minister of India?"]
        ],
        inputs=question_box
    )

    with gr.Row():

        with gr.Column():

            generated_json = gr.JSON(
                label="Generated JSON"
            )

            provenance_box = gr.JSON(
                label="Provenance"
            )

        with gr.Column():

            explanation_box = gr.Textbox(
                label="Query Explanation",
                lines=5
            )

            answer_box = gr.Textbox(
                label="Answer",
                lines=3
            )

    with gr.Row():

        confidence_box = gr.Number(
            label="Confidence Score"
        )

        review_box = gr.Textbox(
            label="Review Status"
        )

    chart_box = gr.Image(
        label="Generated Chart"
    )

    ask_button.click(
        fn=chat,
        inputs=question_box,
        outputs=[
            generated_json,
            explanation_box,
            answer_box,
            provenance_box,
            chart_box,
            confidence_box,
            review_box
        ]
    )

    question_box.submit(
        fn=chat,
        inputs=question_box,
        outputs=[
            generated_json,
            explanation_box,
            answer_box,
            provenance_box,
            chart_box,
            confidence_box,
            review_box
        ]
    )


if __name__ == "__main__":

    demo.launch()