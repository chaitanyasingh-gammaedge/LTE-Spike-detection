DROP TABLE IF EXISTS lte_cells_raw;
CREATE TABLE lte_cells_raw (
    id SERIAL PRIMARY KEY,
    time TIMESTAMP,
    eNodeB_Name TEXT,
    Cell_FDD_TDD_Indication TEXT,
    Cell_Name TEXT,
    LocalCell_Id INTEGER,
    Downlink_PRB_utilization_percent DOUBLE PRECISION,
    Uplink_PRB_utilization_percent DOUBLE PRECISION,
    Avg_Connected_User_LTE DOUBLE PRECISION,
    Avg_Active_User_LTE DOUBLE PRECISION,
    DL_Avg_User_Throughput_kbps DOUBLE PRECISION,
    DL_Cell_Throughput_kbps DOUBLE PRECISION,
    UL_Cell_Throughput_kbps DOUBLE PRECISION,
    UL_Avg_User_Throughput_kbps DOUBLE PRECISION,
    Average_Interference_PRB0 DOUBLE PRECISION,
    Average_Interference_PRB1_8 DOUBLE PRECISION,
    Average_Interference_PRB17_24 DOUBLE PRECISION,
    Average_Interference_PRB25_32 DOUBLE PRECISION,
    Average_Interference_PRB33_40 DOUBLE PRECISION,
    Average_Interference_PRB41_48 DOUBLE PRECISION,
    Average_Interference_PRB49 DOUBLE PRECISION,
    Average_Interference_PRB9_16 DOUBLE PRECISION,
    VoLTE_InterFreq_Handover_Success_Rate_N DOUBLE PRECISION,
    VoLTE_IntraFreq_Handover_Success_Rate_N DOUBLE PRECISION,
    Handover_Success_rate_LTE DOUBLE PRECISION,
    Inter_RAT_Handover_Out_Success_Rate_LTE_to_GERAN DOUBLE PRECISION,
    Inter_RAT_Handover_Out_Success_Rate_LTE_to_GSM DOUBLE PRECISION,
    Inter_RAT_Handover_Out_Success_Rate_LTE_to_WCDMA DOUBLE PRECISION,
    Inter_frequency_Handover_Out_Success_Rate DOUBLE PRECISION,
    Intra_frequency_Handover_Out_Success_Rate DOUBLE PRECISION,
    RRC_Setup_SR_percent DOUBLE PRECISION,
    VOLTE_DL_packet_loss_rate_percent DOUBLE PRECISION,
    VOLTE_UL_packet_loss_rate_percent DOUBLE PRECISION,
    DL_Traffic_Volume_MB DOUBLE PRECISION,
    UL_Traffic_Volume_MB DOUBLE PRECISION,
    VoLTE_Traffic_Erl DOUBLE PRECISION
);


DROP TABLE IF EXISTS lte_cells_processed;
CREATE TABLE lte_cells_processed (
    id SERIAL PRIMARY KEY,
    time TIMESTAMP,
    eNodeB_Name TEXT,
    Cell_FDD_TDD_Indication TEXT,
    Cell_Name TEXT,
    LocalCell_Id INTEGER,
    Downlink_PRB_utilization_percent DOUBLE PRECISION,
    Uplink_PRB_utilization_percent DOUBLE PRECISION,
    Avg_Connected_User_LTE DOUBLE PRECISION,
    Avg_Active_User_LTE DOUBLE PRECISION,
    DL_Avg_User_Throughput_kbps DOUBLE PRECISION,
    DL_Cell_Throughput_kbps DOUBLE PRECISION,
    UL_Cell_Throughput_kbps DOUBLE PRECISION,
    UL_Avg_User_Throughput_kbps DOUBLE PRECISION,
    VOLTE_DL_packet_loss_rate_percent DOUBLE PRECISION,
    VOLTE_UL_packet_loss_rate_percent DOUBLE PRECISION,
    DL_Traffic_Volume_MB DOUBLE PRECISION,
    UL_Traffic_Volume_MB DOUBLE PRECISION,
    VoLTE_Traffic_Erl DOUBLE PRECISION,

    -- Feature engineered columns
    Hour INTEGER,
    Day INTEGER,
    Month INTEGER,
    DayOfWeek TEXT,
    Total_Traffic_MB DOUBLE PRECISION,
    PRB_Util_Avg_percent DOUBLE PRECISION,
    Throughput_Efficiency DOUBLE PRECISION,
    Avg_Packet_Loss_percent DOUBLE PRECISION,
    PRB_Util_Ratio DOUBLE PRECISION,
    User_Activity_Ratio DOUBLE PRECISION,
    Traffic_MA DOUBLE PRECISION,
    Traffic_Change DOUBLE PRECISION,
    Spike_Flag BOOLEAN,
    Possible_Spike BOOLEAN
);



DROP TABLE IF EXISTS lte_spike_detection;
CREATE TABLE lte_spike_detection (
    id SERIAL PRIMARY KEY,
    time TIMESTAMP,
    cell_name TEXT,
    metric_name TEXT,
    metric_value DOUBLE PRECISION,
    is_spike BOOLEAN,
    model_name TEXT,
    score DOUBLE PRECISION
);

