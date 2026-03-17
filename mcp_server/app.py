import gradio as gr
from common.style_print import GREEN, YELLOW, RESET

# -----------------------------------------------------------------------------
# Import Tools
# -----------------------------------------------------------------------------
from tools.explanation_tool import explain_concept
from tools.summarization_tool import summarize_text
from tools.flash_cards_tool import generate_flashcards
from tools.quiz_tool import quiz_me

# -----------------------------------------------------------------------------
# Web UI with Gradio - Launch in the browser window to interact with the tools
# -----------------------------------------------------------------------------
def build_demo():
    with gr.Blocks() as demo:
        gr.Markdown("# AI Tutor MCP Toolkit – Demo Console")
        with gr.Tab("Explain Concept"):
            q = gr.Textbox(label="Concept / Question")
            lvl = gr.Slider(1, 5, value=3, step=1, label="Explanation Level")
            out1 = gr.Markdown()
            gr.Button("Explain").click(explain_concept, inputs=[q, lvl], outputs=out1)
        with gr.Tab("Summarize Text"):
            txt = gr.Textbox(lines=8, label="Long Text")
            ratio = gr.Slider(0.1, 0.8, value=0.3, step=0.05, label="Compression Ratio")
            out2 = gr.Markdown()
            gr.Button("Summarize").click(summarize_text, inputs=[txt, ratio], outputs=out2)
        with gr.Tab("Flashcards"):
            topic_fc = gr.Textbox(label="Topic")
            n_fc = gr.Slider(1, 20, value=5, step=1, label="# Cards")
            out3 = gr.Markdown()
            gr.Button("Generate").click(generate_flashcards, inputs=[topic_fc, n_fc], outputs=out3)
        with gr.Tab("Quiz Me"):
            topic_q = gr.Textbox(label="Topic")
            lvl_q = gr.Slider(1, 5, value=3, step=1, label="Difficulty Level")
            n_q = gr.Slider(1, 15, value=5, step=1, label="# Questions")
            out4 = gr.Markdown()
            gr.Button("Start Quiz").click(quiz_me, inputs=[topic_q, lvl_q, n_q], outputs=out4)
    return demo


if __name__ == "__main__":
    print(f"{YELLOW} Starting AI Tutor MCP Toolkit. Launching web UI at http://localhost:7860/ ...{RESET}")
    # Launch the Gradio app, accessible on the local network for testing with the MCP Client
    build_demo().launch(server_name = "0.0.0.0", mcp_server = True, share = True)
