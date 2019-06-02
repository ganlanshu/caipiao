CREATE TABLE lottery_score (id INTEGER PRIMARY KEY AUTOINCREMENT, 
    trade_id int not null, 
    trade_no char(50), 
    trade_event char(50), 
    trade_start text not NULL, 
    team_l char(50), 
    team_r char(50), 
    concede_point int, 
    score_win real, 
    score_draw real, 
    score_lose real, 
    extra_field text, 
    created_time text not null
);


CREATE TABLE lottery_score_result (id INTEGER PRIMARY KEY AUTOINCREMENT,
    trade_id int not null,
    team_score char(10),
    concede_point int,
    team_l_result int,
    extra_score char(50),
    created_time text not null
);

