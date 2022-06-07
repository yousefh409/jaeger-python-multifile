#!/usr/bin/python3.6
import sys
import os
print(sys.version)

from opentelemetry import propagators, trace
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
import time
from utils import funcUtil

provider = TracerProvider(resource=Resource.create({SERVICE_NAME: "Jenkins Jaeger Test, Python Script"}))
otlp_exporter = OTLPSpanExporter(endpoint=os.environ.get('OTLP_ENDPOINT'), insecure=True)
span_processor = BatchSpanProcessor(otlp_exporter)
processor = BatchSpanProcessor(ConsoleSpanExporter())
provider.add_span_processor(processor)
provider.add_span_processor(span_processor)
trace.set_tracer_provider(provider)

tracer = trace.get_tracer(__name__)

def funcA():
    with tracer.start_as_current_span("funcA"):
        time.sleep(1)
        funcB()

def funcB():
    with tracer.start_as_current_span("funcB"):
        time.sleep(3)
        funcC()
        funcD()

def funcC():
    with tracer.start_as_current_span("funcC"):
        print("Hello world")

def funcD():
    with tracer.start_as_current_span("funcD"):
        time.sleep(1)
        funcUtil()

funcA()