from coding_harness.orchestration import compiled_harness


try:
    compiled_harness.get_graph(xray=True).draw_png(output_file_path="graph.png")
except Exception as e:
    print(f"Error generating graph.png: {e}")