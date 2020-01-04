# Copyright (C) 2020 - Present, OPPO Mobile Comm Corp., Ltd. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

set -e
ROOT=`dirname "$(realpath $0)"`

print_usage()
{
    echo
    echo "Unit Test Running Script..."
    echo
    echo "`basename $0` unit-test-name"
    echo
    echo "Example: `basename $0` resnet18"
    echo
}

if [ $# -eq 0 ]; then
    print_usage
    exit 1
fi

${ROOT}/gradlew installDebugAndroidTest

adb shell am instrument -w -e class com.oppo.seattle.snndemo.NativeTests#$1 com.innopeaktech.seattle.snndemo.test/androidx.test.runner.AndroidJUnitRunner