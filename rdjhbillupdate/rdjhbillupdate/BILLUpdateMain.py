from pyrda.dbms.rds import RdClient


# 收款单 -- 汇票等级
def rds_receipt_draft_grade(sync_date, settlement_method, jh_token):
    jh_app = RdClient(token=jh_token)
    sql = f"""
            -- select pt.FBILLNO,pt.FDATE,pt.F_NLJ_DRAFTGRADE AS '收款单汇票等级',vables.FBILLNO as '票据流水号',vables.DC_I_DRAFTGRADE as '应收票据收款等级',settlement.FNAME
            update pt 
            set pt.F_NLJ_DRAFTGRADE = vables.DC_I_DRAFTGRADE
            from rds_vw_receipt pt
            inner join rds_vw_receivables vables
            on pt.FBILLID = vables.FID
            inner join rds_vw_settlement_method settlement
            on settlement.FID = pt.FSETTLETYPEID
            -- where settlement.FNAME = '银行电子承兑汇票' 
            where settlement.FNAME = '{settlement_method}'
            and vables.DC_I_DRAFTGRADE != pt.F_NLJ_DRAFTGRADE
            -- and pt.FBILLNO = 'SKD00000365';
            and pt.FDATE = '{sync_date}';
            """

    # res = jh_app.select(sql)
    # print(res)

    jh_app.update(sql)


# 收款单 -- 我方银行账号
def rds_receipt_bank_account(sync_date, settlement_method, jh_token):
    jh_app = RdClient(token=jh_token)
    sql = f"""
            -- select pt.FBILLNO,pt.FDATE,pt.F_NLJ_DRAFTGRADE AS '收款单汇票等级',vables.FBILLNO as '票据流水号',vables.DC_I_DRAFTGRADE as '应收票据收款等级',settlement.FNAME
            update pt 
            set pt.FACCOUNTID = vables.FRECBANKACNTID
            from rds_vw_receipt pt
            inner join rds_vw_receivables vables
            on pt.FBILLID = vables.FID
            inner join rds_vw_settlement_method settlement
            on settlement.FID = pt.FSETTLETYPEID
            -- where settlement.FNAME = '银行电子承兑汇票' 
            where settlement.FNAME = '{settlement_method}'
            and pt.FACCOUNTID != vables.FRECBANKACNTID
            -- and pt.FBILLNO = 'SKD00000365';
            and pt.FDATE = '{sync_date}';
            """

    # res = jh_app.select(sql)
    # print(res)

    jh_app.update(sql)


# 付款单 --汇票等级，电票银行账号
def rds_pay_draft_grade(sync_date, settlement_method, jh_token):
    jh_app = RdClient(token=jh_token)
    sql = f"""
            -- select pay.FBILLNO,pay.FDATE,pay.F_NLJ_DRAFTGRADE AS '付款单汇票等级',pay.FTK_BAK_NO as '电票银行账号',
            -- vables.FBILLNO as '票据流水号',vables.DC_I_DRAFTGRADE as '应收票据收款等级',vables.FRECBANKACNTID as '收款银行账号',settlement.FNAME
            update pay
            set pay.F_NLJ_DRAFTGRADE = vables.DC_I_DRAFTGRADE,
            pay.FTK_BAK_NO = vables.FRECBANKACNTID
            from rds_vw_pay pay
            inner join rds_vw_receivables vables
            on pay.FRECEIVEBLEBILLID = vables.FID
            inner join rds_vw_settlement_method settlement
            on settlement.FID = pay.FSETTLETYPEID
            where settlement.FNAME = '{settlement_method}'
            and (vables.DC_I_DRAFTGRADE != pay.F_NLJ_DRAFTGRADE or pay.FTK_BAK_NO != vables.FRECBANKACNTID)
            -- and pay.FBILLNO = 'FKD00000111';
            and pay.FDATE = '{sync_date}'; 
            """

    # res = jh_app.select(sql)
    # print(res)
    # print(sql)
    jh_app.update(sql)


# 付款单 --我方银行账号
def rds_pay_bank_account(sync_date, settlement_method, jh_token):
    jh_app = RdClient(token=jh_token)
    sql = f"""
            -- select pay.FBILLNO,pay.FDATE,pay.F_NLJ_DRAFTGRADE AS '付款单汇票等级',pay.FTK_BAK_NO as '电票银行账号',
            -- vables.FBILLNO as '票据流水号',vables.DC_I_DRAFTGRADE as '应收票据收款等级',vables.FRECBANKACNTID as '收款银行账号',settlement.FNAME
            update pay
            set pay.FACCOUNTID = vables.FRECBANKACNTID
            from rds_vw_pay pay
            inner join rds_vw_receivables vables
            on pay.FRECEIVEBLEBILLID = vables.FID
            inner join rds_vw_settlement_method settlement
            on settlement.FID = pay.FSETTLETYPEID
            where settlement.FNAME = '{settlement_method}'
            and pay.FACCOUNTID != vables.FRECBANKACNTID
            -- and pay.FBILLNO = 'FKD00000111';
            and pay.FDATE = '{sync_date}'; 
            """

    # res = jh_app.select(sql)
    # print(res)
    # print(sql)
    jh_app.update(sql)


# 应收票据结算单
def rds_receivable_settlement(sync_date, document_type, jh_token):
    jh_app = RdClient(token=jh_token)
    sql = f"""
            -- select settlement.FBILLNO,settlement.FDATE,settlement.F_NLJ_DRAFTGRADE,vables.FBILLNO,vables.DC_I_DRAFTGRADE,type.FNAME
            update settlement
            set settlement.F_NLJ_DRAFTGRADE = vables.DC_I_DRAFTGRADE
            from rds_vw_settlement settlement
            inner join rds_vw_receivables vables
            on settlement.FRECBILLID = vables.FID
            inner join rds_vw_billtype type
            on settlement.FBILLTYPEID = type.FBILLTYPEID
            where type.FNAME = '{document_type}'
            and vables.DC_I_DRAFTGRADE != settlement.F_NLJ_DRAFTGRADE
            -- and settlement.FBILLNO = 'BRJS4767'
            and settlement.FDATE = '{sync_date}'
            """

    # res = jh_app.select(sql)
    # print(res)

    jh_app.update(sql)


def main(date, token):
    # rds_receipt_draft_grade(date, '银行电子承兑汇票', token)
    # rds_receipt_bank_account(date, '银行电子承兑汇票', token)
    # rds_receipt_draft_grade(date, '银行纸质承兑汇票', token)
    # rds_receipt_bank_account(date, '银行纸质承兑汇票', token)
    # rds_pay_draft_grade(date, '应收票据背书', token)
    # rds_pay_bank_account(date, '应收票据背书', token)
    rds_receivable_settlement(date, '应收票据背书', token)
    # rds_receivable_settlement(date, '应收票据到期收款', token)
    # rds_receivable_settlement(date, '应收票据贴现', token)
    # rds_receivable_settlement(date, '应收票据退票', token)


if __name__ == '__main__':
    jh_test_token = 'F91CF3E3-8962-47F2-823F-C5CCAAFC66CA'
    main('2023-3-16', jh_test_token)

    # jh_token = 'C0426D23-1927-4314-8736-A74B2EF7A039'
    # main('2020-3-20', jh_token)

    # rds_receipt_draft_grade('2019-6-26', '银行电子承兑汇票', jh_test_token)
    # rds_receipt_bank_account('2019-6-26', '银行电子承兑汇票', jh_test_token)
    # rds_receipt_draft_grade('2019-6-13', '银行纸质承兑汇票', jh_test_token)
    # rds_receipt_bank_account('2019-6-13', '银行纸质承兑汇票', jh_test_token)
    # rds_pay_draft_grade('2020-3-20', '应收票据背书', jh_test_token)
    # rds_pay_bank_account('2020-3-20', '应收票据背书', jh_test_token)
    # rds_receivable_settlement('2023-3-2', '应收票据背书', jh_test_token)
    # rds_receivable_settlement('2023-3-6', '应收票据到期收款', jh_test_token)
    # rds_receivable_settlement('2023-2-15', '应收票据贴现', jh_test_token)
    # rds_receivable_settlement('2021-6-1', '应收票据退票', jh_test_token)
