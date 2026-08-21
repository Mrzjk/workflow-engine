from app.runtime.tracing import TraceRecorder
def test_trace_recorder_retains_node_input_and_output():
    recorder=TraceRecorder(); span=recorder.start("llm_1","llm",{"input":"hello"}); recorder.finish(span,{"output":"world"})
    assert span.status=="success" and span.input["input"]=="hello" and span.output=={"output":"world"}
