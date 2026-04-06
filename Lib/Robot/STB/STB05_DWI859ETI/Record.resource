*** Settings ***
Library    Process
Library    OperatingSystem
Library    DateTime
Library    String
Library    Collections

*** Variables ***
${FFMPEG}         ffmpeg
${VIDEO_DEVICE}   /dev/video0
${VIDEO_SIZE}     1920x1080
${PRESET}         veryfast
${CRF}            23
${FPS}            15
${OUTPUT_DIR}     /home/ltts/Documents/evqual_automation/agentLinuxSTB2/workspace/Record/Etisalat_Linux_STB2
${FILE_NAME}      EtisalatSTB
${FORMAT}         %Y%m%d-%H%M%S
#${BUCKET}         s
#${PREFIX}         https://elasticbeanstalk-ap-south-1-509040541908.s3.ap-south-1.amazonaws.com/EvQUAL/Dev/

*** Keywords ***
Start STB Screen Recording
    [Arguments]    ${port}=1
    Create Directory    ${OUTPUT_DIR}

    ${TS}=      Get Time             result_format=${FORMAT}
    #${safe}=    Replace String       ${TEST NAME}    ${SPACE}    _
    ${rec_file}=    Set Variable     ${OUTPUT_DIR}/${FILE_NAME}-${ts}.mp4  
    ${Record_file}=    Set Variable     ${FILE_NAME}-${TS}.mp4
    Set Suite Variable    ${Record_file}    ${Record_file}
    Log    Timestamp: ${ts}

    ${STB_REC}=    Start Process
    ...    ${FFMPEG}
    ...    -f              v4l2
    ...    -input_format   yuyv422
    ...    -video_size     ${VIDEO_SIZE}
    ...    -i              ${VIDEO_DEVICE}
    ...    -c:v            libx264
    ...    -preset         ${PRESET}
    ...    -crf            ${CRF}
    ...    -pix_fmt        yuv420p
    ...    -r              ${FPS}
    ...    ${REC_FILE}
    ...    stdout=NONE     stderr=NONE

    Set Suite Variable    ${REC_FILE}    ${REC_FILE}
    Set Suite Variable    ${STB_REC}    ${STB_REC}

Stop STB Screen Recording for Failed Testcases
    ${PROCEDURE}=    Get Variable Value    ${STB_REC}
    Terminate Process    ${PROCEDURE}
    Wait For Process     ${PROCEDURE}

    ${STATUS}=  Get Variable Value    ${TEST STATUS}
    Run Keyword If    '${STATUS}' != 'FAIL'
    ...    Remove File    ${REC_FILE}
    ...    ELSE
    #...    Log    <a href="https://elasticbeanstalk-ap-south-1-509040541908.s3.ap-south-1.amazonaws.com//EvQUAL/Test/${Record_file}" target="_blank">View Recording</a>    html=True
    #Log    <video width="640" controls><source src="https://elasticbeanstalk-ap-south-1-509040541908.s3.ap-south-1.amazonaws.com//EvQUAL/Test/${Record_file}" type="video/mp4">Your browser does not support the video tag.</video>    html=True

    

Stop STB Screen Recording for both pass and fail 
    ${proc}=    Get Variable Value    ${STB_REC}
    Terminate Process    ${proc}
    Wait For Process     ${proc}
    #Log    <a href="https://elasticbeanstalk-ap-south-1-509040541908.s3.ap-south-1.amazonaws.com//EvQUAL/Test/${Record_file}" target="_blank">View Recording</a>    html=True
    #Log    <video width="640" controls><source src="https://elasticbeanstalk-ap-south-1-509040541908.s3.ap-south-1.amazonaws.com//EvQUAL/Test/${Record_file}" type="video/mp4">Your browser does not support the video tag.</video>    html=True
    #Run Keyword  Run Video Caption Script And Log Video


#Show Testcase Recording
    #[Arguments]    ${file}
    #Log    <b>Recording:</b><br><video width="640" controls><source src="${PREFIX}${Record_file}" type="video/mp4">Your browser does not support the video tag.</video>    html=True
    #Log    <a href="../agent8dut4/Report//${REC_FILE}" target="_blank">View Recording</a>    html=True


