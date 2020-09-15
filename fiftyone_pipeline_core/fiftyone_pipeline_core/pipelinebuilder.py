# *********************************************************************
# This Original Work is copyright of 51 Degrees Mobile Experts Limited.
# Copyright 2019 51 Degrees Mobile Experts Limited, 5 Charlotte Close,
# Caversham, Reading, Berkshire, United Kingdom RG4 7BY.
#
# This Original Work is licensed under the European Union Public Licence (EUPL)
# v.1.2 and is subject to its terms as set out below.
#
# If a copy of the EUPL was not distributed with this file, You can obtain
# one at https://opensource.org/licenses/EUPL-1.2.
#
# The 'Compatible Licences' set out in the Appendix to the EUPL (as may be
# amended by the European Commission) shall be deemed incompatible for
# the purposes of the Work and the provisions of the compatibility
# clause in Article 5 of the EUPL shall not apply.
#
# If using the Work as, or as part of, a network application, by
# including the attribution notice(s) required under Article 5 of the EUPL
# in the end user terms of the application under an appropriate heading,
# such notice(s) shall fulfill the requirements of that article.
# ********************************************************************

from .pipeline import Pipeline
from .logger import Logger
from .javascriptbuilder import JavascriptBuilderElement
from .jsonbundler import JSONBundlerElement
from .sequenceelement import SequenceElement
import json


class PipelineBuilder:
    """
    A PipelineBuilder generates a Pipeline object
    Before construction of the Pipeline, FlowElements are added to it
    There are also options for how JavaScript is output from the Pipeline

    """

    def __init__(self, settings={}):
        """
        Pipeline Builder constructor.
        @type settings: dictionary
        @param settings : settings for the pipeline builder including:
        `addJavaScriptBuilder (Bool)` - Whether to add the JavaScriptBuilder to the pipeline
        (default true)
        `javascriptBuilderSettings (dict)` - Settings for the JavaScriptBuilder engine 
        @rtype: PipelineBuilder
        @returns: Returns a Pipeline Builder

        """

        self.flow_elements = []
        self.logger = Logger()

        if "addJavaScriptBuilder" in settings:
            self.add_javaScriptbuilder = settings["addJavascriptBuilder"]
        else:
            self.add_javaScriptbuilder = True
       
      
        if "javascriptBuilderSettings" in settings:
            self.javascriptbuilder_settings = settings["javascriptBuilderSettings"]



    def get_javascript_elements(self):
        """
        Adds the JavaScriptBuilder, JSONBundler and SequenceElement to the pipeline if
        If addJavascriptBuilder is set to true (the default)
        @rtype: list
        @returns: Returns a list of FlowElements     
        """
        
        flow_elements = []

        if (self.add_javaScriptbuilder):

            flow_elements.append(SequenceElement())
            flow_elements.append(JSONBundlerElement())
    
            if (hasattr(self, "javascriptbuilder_settings")):
                flow_elements.append(JavascriptBuilderElement(self.javascriptbuilder_settings))
            else:
                flow_elements.append(JavascriptBuilderElement())
   
        return flow_elements

    def add(self, flow_element):
        """
        Add a flow_element to a list of flowElements be used in a pipeline.
        
        @type flow_element: FlowElement
        @param flow_element: flowElement to be added to the pipeline

        @rtype: PipelineBuilder
        @returns: Returns the pipleine builder with the specified flowElement added to it's list of flowElements.

        """

        self.flow_elements.append(flow_element)

        return self

    def build(self):
        """
        Construct an immutable Pipeline using the list of flowElements, (Engines) and (Logger) currently in this Pipeline Builder.
        Call build after all items to be included in the pipeline have been added.

        @rtype: Pipeline
        @returns: Returns a Pipeline

        """

        self.flow_elements.extend(self.get_javascript_elements())

        return Pipeline(self.flow_elements, logger=self.logger)

    def add_logger(self, logger):
        """
        Add an instance of the logger class to the pipeline.

        @type logger: Logger
        @param logger: Logger to be added to the pipeline

        @rtype: PipelineBuilder
        @returns: Returns the pipeline builder with the specified Logger added.
        
        """

        self.logger = logger

        return self
