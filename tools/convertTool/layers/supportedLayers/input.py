# Copyright (C) 2020 - Present, OPPO Mobile Comm Corp., Ltd. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
from config.formatConfig.supportedFormats import SUPPORTED_FORMATS
from config.frameworkConfig.supportedFrameworks import SUPPORTED_COMPATIBLE_FRAMEWORKS
from convertProcessor.processorConfig import processConfig
from convertProcessor.processorConfig.processConfig import COMPATIBLE_FRAMEWORK
from layers.supportedLayers import layerHelper
from layers.supportedLayers.layer import Layer


class Input(Layer):
    layerInfo = dict()

    def handleLayer(self, **kwargs):
        layername = kwargs['layername']
        layerinfo = kwargs['layerinfo']
        self.layerInfo = layerinfo
        # print(layerinfo)

    def getConvertedJSONForLayer(self):
        if COMPATIBLE_FRAMEWORK == SUPPORTED_COMPATIBLE_FRAMEWORKS.SNN:
            if processConfig.getCurrentFormat() == SUPPORTED_FORMATS.H5ToJson:
                self.getSNNCompatibleJSONFromH5()
            elif processConfig.getCurrentFormat() == SUPPORTED_FORMATS.ONNXToJson:
                self.getSNNCompatibleJSONFromONNX()

    def getSNNCompatibleJSONFromONNX(self):
        layerJSON = dict()
        layername = self.layerInfo['name']
        layerJSON['name'] = layername
        layerJSON['type'] = 'InputLayer'
        tensorType = self.layerInfo['type']['tensorType']
        # print(tensorType)
        if 'shape' in tensorType:
            shape = tensorType['shape']
            dims = shape['dim']
            shapes = []
            for d in dims:
                # print(d)
                if 'dimValue' in d.keys():
                    shapes.append(d['dimValue'])
                elif 'dimParam' in d.keys():
                    shapes.append(d['dimParam'])
            layerJSON['Input Height'] = int(shapes[2])
            layerJSON['Input Weight'] = int(shapes[3])
            layerJSON['outputPlanes'] = int(shapes[1])

        #TODO : Handle else case if shape not present
        self.addInbounds(layerJSON)
        layerHelper.layersToJSON[layername] = layerJSON

    def getSNNCompatibleJSONFromH5(self):
        layerJSON = dict()
        layername = self.layerInfo['config']['name']
        layerJSON['name'] = layername
        layerJSON['type'] = self.layerInfo['class_name']
        if type(self.layerInfo['config']['batch_input_shape'][1]) is None.__class__:
            layerJSON["Input Height"] = 640
            layerJSON["Input Width"] = 360
        else:
            layerJSON["Input Height"] = self.layerInfo['config']['batch_input_shape'][1]
            layerJSON["Input Width"] = self.layerInfo['config']['batch_input_shape'][2]
        layerJSON["outputPlanes"] = self.layerInfo['config']['batch_input_shape'][3]
        if 'batch_input_shape' in self.layerInfo['config']:
            layerJSON['batch_input_shape'] = self.layerInfo['config']['batch_input_shape']
        self.addInbounds(layerJSON)
        layerHelper.layersToJSON[layername] = layerJSON
        # print(layerJSON)

    def addInbounds(self, layerJSON):
        layerJSON['inbounds'] = []

        if processConfig.getCurrentFormat() == SUPPORTED_FORMATS.H5ToJson:
            currentInbounds = self.layerInfo['inbound_nodes']
            for inboundList in currentInbounds:
                for inbound in inboundList:
                    inboundLayername = inbound[0]
                    layerJSON['inbounds'].append(inboundLayername)

            # print(layerJSON['inbounds'])
        elif processConfig.getCurrentFormat() == SUPPORTED_FORMATS.ONNXToJson:
            if 'input' in self.layerInfo:
                pass