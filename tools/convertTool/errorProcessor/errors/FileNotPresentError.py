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
import sys

from errorProcessor.errorConfig.errorTypes import ErrorType
from errorProcessor.errors import error


class FileNotPresentError(error.Error):

    errorType = ErrorType.UNRECOVERABLE
    errorMessage = "File not found. Please provide model file."

    def handleError(self, **kwargs):
        msg = kwargs.get('filepath') + " " + self.errorMessage
        raise Exception(msg)
        sys.exit()
