import datetime
def session_retrieval1(user_dic,users,m_acc,result):
    sessid = ""
    account = ""
    #result = read_model_identify(account_model, acc_o)
    label_info = result.get("label_info", {})
    if label_info.get("日志类型") == "账号登录":
        data = result.get("data", {})
        user_infos = {}
        token_container = []
        if not data:
            return user_dic, account,users,"",m_acc
        for http_pos, action_value in data.items():
            for action, value_lst in action_value.items():
                if "会话ID" not in value_lst or "账户名" not in value_lst:
                    # 如果不存在就可能存在两个合并接口的账户 或者是没有标注，可以等待一会
                    for name,value in value_lst.items():
                        m_acc[name] = value[0]
                else:
                    for name, value in value_lst.items():
                        if name != "会话ID":
                            if len(value) >= 1:
                                user_infos[name] = value[0]
                        else:
                            token_container = value
        if len(m_acc) ==2:
            # 如果是两个数据就表明账户跟会话ID都存储完毕，然后往最终字典靠拢
            for name,value in m_acc.items():
                if name!="会话ID":
                    user_infos[name]=value
                else:
                    token_container.append(value)
            m_acc = {}
        user_infos["date"] = datetime.datetime.now()
        if token_container:
            for jsessionid in token_container:
                user_dic[jsessionid]= user_infos
                account = user_infos.get("账户名")
                sessid = jsessionid
    #Delete 注释 by rzc on 2024-08-26 16:37:29
#解除注释 by rzc on 2024-08-26 16:55:24
    else:
        # 获取到的是请求体中的 session_ID
        data = result.get("data", {})
        if data:
            for pos, pos_data in data.items():
                for action, action_data in pos_data.items():
                    for ch_name, value_list in action_data.items():
                        if ch_name == "会话ID" and value_list:
                            sessid = value_list[0]
    if sessid and sessid in user_dic:
        user_info = user_dic.get(sessid, {})
        account = user_info.get("账户名", "")
        if "user_info" in user_info:
            users = user_info.get("user_info")
    return user_dic, account,users,sessid,m_acc

if __name__ == "__main__":
    user_dic = {}

    users = {}
    m_acc = {}
    res_list = [

        {'data': {'response_headers': {'操作': {'账户名': ['superFBI']}}}, 'label_info': {'日志类型': '账号登录'}, 'map_tree': None},
        {'data': {'response_headers': {'返回结果': {'会话ID': ['f376adbfb64f9ea8df8f44c7ebfab993']}}}, 'label_info': {'日志类型': '账号登录'}, 'map_tree': None}    ]
    for res in res_list:
        user_dic, account,users,sessid,m_acc = session_retrieval1(user_dic,users,m_acc,res)
        print(user_dic)
        print(m_acc)
    import pickle
    with open("./operevent_rcl.pkl",'rb')as fp:
        res_list = pickle.load(fp)
        print(res_list)