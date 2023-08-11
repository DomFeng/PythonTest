import sys
import time

import pymysql

# help
print("==========================工具说明==========================")
print("请输入以下信息，进行委托流水生成：")
print("productNum           产品代码")
print("productAcctNum       资产单元")
print("PortfolioNum         投资组合")
print("bstype               买卖方向，例:买入B，卖出S")
print("exchid               交易市场，例:上海0，深圳1")
print("counts               生成数量")
print("===========================================================")

# init variable
productNum = input("Please enter productNum: ")
productAcctNum = input("Please enter productAcctNum: ")
portfolioNum = input("Please enter PortfolioNum: ")
bstype = input("Please enter bstype:")
# 判断bstype是否为B或S，如果不是则重新输入
while bstype != 'B' and bstype != 'S':
    bstype = input("bstype输入错误，请重新输入:")
exchid = input("Please enter exchid:")
counts = input("Please enter insert counts:")
osn = 301070525584400000
sn = 401070525584400000
cn = 304000000
stks = 0
commit_cns = 0

# Connect to MySQL database
db = pymysql.connect(host='127.0.0.1', port=3306, user='coredb', password='coredb', database='coredb',
                     charset="utf8")
print("Connect to MySQL database successfully!")
cursor = db.cursor()

# 获取交易日期
trade_date = "select tradedate from sysconfig;"
cursor.execute(trade_date)
trade_date = cursor.fetchone()
dates = int(str(trade_date[0]) + '160330')
print("交易日：" + str(trade_date[0]))


# 插入openorder表
def make_openorder(productNum, productAcctNum, portfolioNum, bstype, exchid, counts, dates, cursor):
    global osn, commit_cns, cn, stks

    # 定义sql语句
    sql1 = (
        "select productNum, productAcctNum ,PortfolioNum,PortfolioName from bside_pfoliobaseinfo where productNum = %s "
        "and productAcctNum = %s and PortfolioNum = %s;")
    sql2 = "select acctid from bside_account where productAcctNum = %s;"
    sql3 = ("select regId,offerRegId from registration where regId in (select regId from "
            "bside_product_reg where productAcctNum = %s and exchid=%s) limit 1;")
    sql4 = ("select stkId,stkName,exchId,stkType,tradeType from stkinfo s where"
            " stkType ='A0' and tradeType ='A0' and exchid = %s;")

    # Execute query and fetch rows
    cursor.execute(sql1, (productNum, productAcctNum, portfolioNum))
    res1 = cursor.fetchall()

    # 输出查询结果
    # print("======================查询结果======================")
    # print(res1[0][0], res1[0][1], res1[0][2], res1[0][3])
    cursor.execute(sql2, productAcctNum)
    res2 = cursor.fetchall()
    # print(res2[0][0])
    cursor.execute(sql3, (productAcctNum, exchid))
    res3 = cursor.fetchall()
    # print(res3[0][0], res3[0][1])
    cursor.execute(sql4, exchid)
    res4 = cursor.fetchall()
    # print(res4[0][0], res4[0][1], res4[0][2], res4[0][3], res4[0][4])
    # print("===================================================")
    print("openorder插入数据开始！")

    insert_openorder = (
        "INSERT INTO coredb.openorder (OrigSerialNo, OrigSource, OrigChannel, productNum, productAcctNum, "
        "PortfolioNum, PortfolioName, acctid, exchId, regId, offerRegId, stkId, stkName, F_hedgeFlag, "
        "coveredFlag, stkType, tradeType, deskId, BsType, OCFlag, orderTypeFlag, orderTypeDetailFlag, "
        "F_orderPriceType, MktOrderFlag, MktOrderFlagDesc, F_MatchCondition, ThirdContractNo, ContractNum, "
        "orderQty, orderPrice, priceStrategy, tradeFrozenAmt, stockFrozenQty, orderputtingQty, frozenPrice,"
        " ownerType, stopPrice, knockQty, knockAmt, withdrawQty, withdrawOrderFlag, legalFlag, sendFlag, "
        "StatusCode, ErrCode, ErrMsg, openUsedMarginAmt, openFrozMargin, closePNL, OffsetMarginAmt, "
        "PlatformID, localOrderId, BusinessMark, orderSource, instDetailSerialNum, InstructId, basketId, "
        "BatchSerialNo, byPatchSerialNo, occurTime, orderTime, offerTime, OrderMode, FundstkId, optId, "
        "operationMAC, auditOptId, AuditMAC, memo, patchFlag, compactId, SequenceNo, targetDeskId, "
        "targetRegId, appointNo, ThirdSystemId, buy1, sell1, newprice, exchProperty, amendPrice, "
        "totalCommision, accuredInterest, reckoningAmt, lastKnockTime, KnockPrice, riskPendingFlag, "
        "StkProperty, auditTime, SettleReckoningAmt, orderSourceId, AutoCloseFlag, StockHoldFlag, LegSide, "
        "minimalVolume, intelligentSerialNum, MaxPriceLevels, GwSequenceNo, IntelligentType, arbiContractID"
        ", targetTradeFrozenAmt, combineNum, creditFrozenQty, WithdrawPermit, unCreditShareUsableAmt, "
        "unMFUsedAmt, userinfo) VALUES(%s, '3', '', %s, %s, %s, %s, %s, '1', %s, %s, %s, %s, 'SPEC', %s, "
        "%s, %s, '', %s, 'O', '0', '00', "
        "'LIMIT', '', '', '', %s, %s , 100, 11.4000, NULL, 1193.480, 0, 100, 0.0000, '1', 0.0000, 100, "
        "1140.00, 0, 2, 0, 1, 'Fully_Filled', '', '', 0.00, 0.00, 0.00, 0.00, '00', NULL, '0B', 0, 0, '', "
        "'', %s, 0, %s, %s, %s, 0, '', 'test1', 'TerminalId= 000000000000_AMS_aaa652d637464530b2c"
        "06960a6537ef1', NULL, NULL, '', 0, '', 1, '', '', '', '2301', 11.3400, 11.3500, 11.3400, '0', "
        "0.0000, 53.48, 0.00000000, -1193.48, 20230705160331, 11.40000, 'N', '0', -1, -1193.4800, -1, 0, 0,"
        " 0, 0, 0, 0, -1, 'DMA', '', 0.000, 'ALL', 0, '', 0.00, 0.00, '');")

    # 循环插入openorder表，循环次数为counts
    for i in range(int(counts)):
        cursor.execute(insert_openorder, (
            osn, res1[0][0], res1[0][1], res1[0][2], res1[0][3], res2[0][0], res3[0][0], res3[0][1], res4[stks][0],
            res4[stks][1], res4[stks][2], res4[stks][3], res4[stks][4], bstype, cn, cn, osn, dates, dates, dates))
        # print("openorder插入第%s条数据" % (i + 1))

        print("\r", end="")
        progress = round(i/int(counts)*100, 2)
        print("进度: {}%: ".format(progress), "▓" * (int(i/int(counts)*100) // 2), end=" ")
        sys.stdout.flush()

        # 判断commit_cns是否等于1000，如果等于1000，提交一次，否则commit_cns+1
        # if commit_cns == 1000:
        #     db.commit()
        #     commit_cns = 0
        # else:
        #     commit_cns += 1

        osn += 1
        cn += 1
        # if判断result4行数，如果stks小于result4行数，stks+1，否则stks=0
        if stks < len(res4) - 1:
            stks += 1
        else:
            stks = 0

    db.commit()

    # restore the value
    osn = 301070525584400000
    cn = 304000000
    stks = 0
    commit_cns = 0

    print("openorder插入完成！")

    return osn, cn, stks


# 插入openorderdetail表
def make_openorderdetail(productNum, productAcctNum, portfolioNum, bstype, exchid, counts, dates, cursor):
    global osn, sn, cn, stks, commit_cns

    # Query to get 1000 rows of data
    sql1 = (
        "select productNum, productAcctNum ,PortfolioNum,PortfolioName from bside_pfoliobaseinfo where productNum = %s "
        "and productAcctNum = %s and PortfolioNum = %s;")
    sql2 = "select acctid from bside_account where productAcctNum = %s;"
    sql3 = ("select regId,offerRegId from registration where regId in (select regId from "
            "bside_product_reg where productAcctNum = %s and exchid=%s) limit 1;")
    sql4 = ("select stkId,stkName,exchId,stkType,tradeType from stkinfo s where"
            " stkType ='A0' and tradeType ='A0' and exchid = %s;")

    # Execute query and fetch rows
    cursor.execute(sql1, (productNum, productAcctNum, portfolioNum))
    res1 = cursor.fetchall()

    # 输出查询结果
    # print("======================查询结果======================")
    # print(res1[0][0], res1[0][1], res1[0][2], res1[0][3])
    cursor.execute(sql2, productAcctNum)
    res2 = cursor.fetchall()
    # print(res2[0][0])
    cursor.execute(sql3, (productAcctNum, exchid))
    res3 = cursor.fetchall()
    # print(res3[0][0], res3[0][1])
    cursor.execute(sql4, exchid)
    res4 = cursor.fetchall()
    # print(res4[0][0], res4[0][1], res4[0][2], res4[0][3], res4[0][4])
    # print("===================================================")
    print("openorderdetail插入数据开始！")

    insert_openorderdetail = (
        "INSERT INTO coredb.openorderdetail (OrigSerialNo, SerialNo, Source, Channel, productNum, productAcctNum, "
        "PortfolioNum, PortfolioName, exchId, regId, offerRegId, stkId, stkName, F_hedgeFlag, coveredFlag, stkType, "
        "tradeType, deskId, BsType, OCFlag, orderTypeFlag, orderTypeDetailFlag, F_orderPriceType, MktOrderFlag, "
        "MktOrderFlagDesc, F_MatchCondition, OrderFlag, ThirdContractNo, ContractNum, OrigContractNum, ThirdSystemId, "
        "orderQty, orderPrice, optId, operationMAC, withdrawQty, legalFlag, sendFlag, occurTime, orderTime, "
        "knocktime, StatusCode, ErrCode, ErrMsg, memo, FundstkId, SequenceNo, targetDeskId, targetRegId, appointNo, "
        "StkProperty, GwSequenceNo, IntelligentType, OrigModSerialNo, auditOptId, AuditMAC, auditTime, auditMemo, "
        "arbiContractID, clordId, origClordId) VALUES(%s, %s, '3', '', %s, %s, %s, "
        "%s, '1', %s, %s, %s, %s, 'SPEC', %s, %s, %s, '', %s, 'O', '0', '00', "
        "'LIMIT', '', '', '', 'N', %s, %s, '', '2301', 100, 11.4000, 'test1', 'TerminalId= "
        "000000000000_AMS_aaa652d637464530b2c06960a6537ef1', 0, 0, 1, %s, %s, %s, 'Fully_Filled', '', '', "
        "'', '', 1, '', '', '', '0', -1, 'DMA', 0, NULL, NULL, -1, NULL, '', %s, '');")

    # 循环插入openorder表，循环次数为counts
    for i in range(int(counts)):
        cursor.execute(insert_openorderdetail, (
            osn, sn, res1[0][0], res1[0][1], res1[0][2], res2[0][0], res3[0][0], res3[0][1], res4[stks][0],
            res4[stks][1], res4[stks][2], res4[stks][3], res4[stks][4], bstype, cn, cn, dates, dates, dates, cn))
        # print("openorderdetail插入第%s条数据" % (i + 1))
        print("\r", end="")
        progress = round(i/int(counts)*100, 2)
        print("进度: {}%: ".format(progress), "▓" * (int(i/int(counts)*100) // 2), end=" ")
        sys.stdout.flush()
        # 判断commit_cns是否等于1000，如果等于1000，提交一次，否则commit_cns+1
        # if commit_cns == 1000:
        #     db.commit()
        #     commit_cns = 0
        # else:
        #     commit_cns += 1

        osn += 1
        sn += 1
        cn += 1
        # if判断result4行数，如果stks小于result4行数，stks+1，否则stks=0
        if stks < len(res4) - 1:
            stks += 1
        else:
            stks = 0

    db.commit()

    # restore the value
    osn = 301070525584400000
    sn = 401070525584400000
    cn = 304000000
    stks = 0
    commit_cns = 0

    print("openorderdetail插入完成！")

    return osn, cn, stks


# 插入tradingresult表
def make_tradingresult(productNum, productAcctNum, portfolioNum, bstype, exchid, counts, dates, cursor):
    global osn, sn, cn, stks, commit_cns

    # Query to get 1000 rows of data
    sql1 = (
        "select productNum, productAcctNum ,PortfolioNum,PortfolioName from bside_pfoliobaseinfo where productNum = %s "
        "and productAcctNum = %s and PortfolioNum = %s;")
    sql2 = "select acctid from bside_account where productAcctNum = %s;"
    sql3 = ("select regId,offerRegId from registration where regId in (select regId from "
            "bside_product_reg where productAcctNum = %s and exchid=%s) limit 1;")
    sql4 = ("select stkId,stkName,exchId,stkType,tradeType from stkinfo s where"
            " stkType ='A0' and tradeType ='A0' and exchid = %s;")

    # Execute query and fetch rows
    cursor.execute(sql1, (productNum, productAcctNum, portfolioNum))
    res1 = cursor.fetchall()

    # 输出查询结果
    # print("======================查询结果======================")
    # print(res1[0][0], res1[0][1], res1[0][2], res1[0][3])
    cursor.execute(sql2, productAcctNum)
    res2 = cursor.fetchall()
    # print(res2[0][0])
    cursor.execute(sql3, (productAcctNum, exchid))
    res3 = cursor.fetchall()
    # print(res3[0][0], res3[0][1])
    cursor.execute(sql4, exchid)
    res4 = cursor.fetchall()
    # print(res4[0][0], res4[0][1], res4[0][2], res4[0][3], res4[0][4])
    # print("===================================================")
    print("tradingresult插入数据开始！")

    insert_tradingresult = (
        "INSERT INTO coredb.tradingresult (OrigSerialNo, OrigSource, OrigChannel, SerialNo, productNum, "
        "productAcctNum, PortfolioNum, PortfolioName, acctid, exchId, regId, offerRegId, stkId, stkName, F_hedgeFlag, "
        "coveredFlag, stkType, tradeType, deskId, BsType, OCFlag, orderTypeFlag, orderTypeDetailFlag, ReportType, "
        "OrderFlag, knockQty, postQty, knockPrice, knockAmt, fullknockAmt, accuredInterest, knockCode, reckoningAmt, "
        "settleReckoningAmt, ThirdContractNo, ContractNum, openUsedMarginAmt, closePNL, OffsetMarginAmt, stampTax, "
        "tradetransFee, reckoningFee, transRuleFee, handlingFee, stkMngFee, exchtransFee, ventureFee, commision, "
        "otherFee, instDetailSerialNum, InstructId, basketId, BatchSerialNo, ThirdSystemId, NoOrderFlag, ExchRate, "
        "SequenceNo, targetDeskId, targetRegId, appointNo, occurTime, knockTime, postProcessFlag, exchProperty, "
        "totalCommision, F_MatchCondition, F_OrderPriceType, stopPrice, StkProperty, GwSequenceNo, IntelligentType, "
        "arbiContractID, MktOrderFlag, adjustRate) VALUES(%s, '3', '', %s, %s, %s, %s, "
        "%s, %s, '1', %s, %s, %s, %s, 'SPEC', %s, %s, %s, '', %s, 'O', "
        "'0', '00', '1', 'N', 100, 0, 11.4000, 1140.00, 1140.00, 0.00000000, '1', -1193.48, -1193.48, %s, %s, 0.00, "
        "0.00, 0.00, 1.14, 1.14, 1.14, 1.20, 1.14, 1.14, 1.14, 1.14, 50.00, 0.00, 0, '', '', %s, '2301', 'N', "
        "1.000000, 1, '', '', '', %s, %s, 0, '0', 53.48, '', 'LIMIT', 0.0000, '0', -1, 'DMA', '', '', 0.000000);")

    # 循环插入tradingresult表，循环次数为counts
    for i in range(int(counts)):
        cursor.execute(insert_tradingresult, (
            osn, sn, res1[0][0], res1[0][1], res1[0][2], res1[0][3], res2[0][0], res3[0][0], res3[0][1], res4[stks][0],
            res4[stks][1], res4[stks][2], res4[stks][3], res4[stks][4], bstype, cn, cn, osn, dates, dates))
        # print("tradingresult插入第%s条数据" % (i + 1))
        print("\r", end="")
        progress = round(i/int(counts)*100, 2)
        print("进度: {}%: ".format(progress), "▓" * (int(i/int(counts)*100) // 2), end=" ")
        sys.stdout.flush()
        # 判断commit_cns是否等于1000，如果等于1000，提交一次，否则commit_cns+1
        # if commit_cns == 1000:
        #     db.commit()
        #     commit_cns = 0
        # else:
        #     commit_cns += 1

        osn += 1
        sn += 1
        cn += 1
        # if判断result4行数，如果stks小于result4行数，stks+1，否则stks=0
        if stks < len(res4) - 1:
            stks += 1
        else:
            stks = 0

    db.commit()

    # restore the value
    osn = 301070525584400000
    sn = 401070525584400000
    cn = 304000000
    stks = 0
    commit_cns = 0

    print("tradingresult插入完成！")

    return osn, cn, stks


# 创建主方法
if __name__ == '__main__':
    start_time = time.time()  # 记录方法开始时间
    # insert data
    make_openorder(productNum, productAcctNum, portfolioNum, bstype, exchid, counts, dates, cursor)
    make_openorderdetail(productNum, productAcctNum, portfolioNum, bstype, exchid, counts, dates, cursor)
    make_tradingresult(productNum, productAcctNum, portfolioNum, bstype, exchid, counts, dates, cursor)
    end_time = time.time()  # 记录方法结束时间
    elapsed_time = end_time - start_time  # 计算耗时
    print(f"Elapsed time: {elapsed_time:.2f} seconds")
    # Close connection
    cursor.close()
    db.close()

