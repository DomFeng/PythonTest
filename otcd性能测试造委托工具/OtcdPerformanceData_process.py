import threading
from multiprocessing import Process
import time
import pymysql

# Help
print("==========================工具说明==========================")
print("请输入以下信息，进行委托流水生成：")
print("productNum           产品代码")
print("productAcctNum       资产单元")
print("PortfolioNum         投资组合")
print("bstype               买卖方向，例:买入B，卖出S")
print("exchid               交易市场，例:上海0，深圳1")
print("counts               生成数量")
print("===========================================================")

print("是否为收益互换模式yes/no")
is_swap = input("请输入：")

# init variable
productNum = input("Please enter productNum: ")
productAcctNum = input("Please enter productAcctNum: ")
portfolioNum = input("Please enter PortfolioNum: ")

if is_swap == 'yes':
    productNum_B = input("Please enter productNum_B: ")
    productAcctNum_B = input("Please enter productAcctNum_B: ")
    portfolioNum_B = input("Please enter PortfolioNum_B: ")

bstype = input("Please enter bstype:")
# 判断bstype是否为B或S，如果不是则重新输入
while bstype != 'B' and bstype != 'S':
    bstype = input("bstype输入错误，请重新输入:")
exchid = input("Please enter exchid:")
counts = input("Please enter insert counts:")

# datebase config
host = '192.168.1.101'
port = 3700
user = 'root'
password = 'root'
database = 'coredb_v2310'

db_init = pymysql.connect(host=host, port=port, user=user, password=password, database=database,
                          charset="utf8")
print('查最大序列：'+ database)
cursor_init = db_init.cursor()
serial_sql = "select max(OrigSerialNo), max(SerialNo), max(clordId) from openorderdetail;"
cursor_init.execute(serial_sql)
serial = cursor_init.fetchone()
# 如果serial[0]为空，osn=301070525584400000，否则osn=max(OrigSerialNo)+1
if serial[0] is None:
    osn = 301070525584400000
else:
    osn = int(serial[0]) + 10000
# 如果max(SerialNo)为空，sn=401070525584400000，否则sn=max(SerialNo)+1
if serial[1] is None:
    sn = 401070525584400000
else:
    sn = int(serial[1]) + 10000
# 如果max(clordId)为空，cn=304000000，否则cn=max(clordId)+1
if serial[2] is None:
    cn = 304000000
else:
    cn = int(serial[2]) + 10000

cursor_init.close()
db_init.close()

stks = 0
commit_cns = 0
threadnum = 10

local_vars = threading.local()


def singlethread(tag, num, table, insertdata):
    db = pymysql.connect(host=host, port=port, user=user, password=password, database=database,
                         charset="utf8")
    # print("Connect to MySQL database successfully!")
    cursor = db.cursor()
    cursor.executemany(table, insertdata)

    db.commit()
    cursor.close()
    db.close()
    print(f'{tag} 线程 {num} 执行结束')


def startthread(tag, table, insertdata, threadnum, count):
    threaddict = {}
    for num in range(threadnum):
        singleactcount = count // threadnum + 1
        left = singleactcount * num
        right = singleactcount * (num + 1)
        if right > count:
            right = count

        threaddict[num] = threading.Thread(target=singlethread, args=(tag, num, table, insertdata[left:right]))
        print(f'{tag} 线程 {num} 已启动')
        threaddict[num].start()

    for key in threaddict.keys():
        threaddict[key].join()


def make_openorder(productNum, productAcctNum, portfolioNum, bstype, exchid, counts, productNum_B=0, productAcctNum_B=0,
                   portfolioNum_B=0):
    global osn, commit_cns, cn, stks, is_swap
    local_vars.osn = osn
    local_vars.cn = cn
    local_vars.stks = stks
    local_vars.commit_cns = commit_cns
    local_vars.is_swap = is_swap

    db = pymysql.connect(host=host, port=port, user=user, password=password, database=database,
                         charset="utf8")
    cursor = db.cursor()
    # 获取交易日期
    trade_date = "select tradedate from sysconfig;"
    cursor.execute(trade_date)
    trade_date = cursor.fetchone()
    dates = int(str(trade_date[0]) + '160330')
    # print("交易日：" + str(trade_date[0]))

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

    if is_swap == 'yes':
        cursor.execute(sql1, (productNum_B, productAcctNum_B, portfolioNum_B))
        res1_B = cursor.fetchall()
        cursor.execute(sql2, productAcctNum_B)
        res2_B = cursor.fetchall()
        cursor.execute(sql3, (productAcctNum_B, exchid))
        res3_B = cursor.fetchall()

    cursor.execute(sql4, exchid)
    res4 = cursor.fetchall()
    print('证券数量为：' + str(len(res4)))
    # print(res4[0][0], res4[0][1], res4[0][2], res4[0][3], res4[0][4])
    # print("===================================================")
    cursor.close()
    db.close()
    print("openorder插入数据开始，请稍等...")

    insert_openorder = (
        "INSERT INTO openorder (OrigSerialNo, OrigSource, OrigChannel, productNum, productAcctNum, "
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

    datalist = []
    for local_vars.i in range(int(counts)):
        datalist.append((
            local_vars.osn, res1[0][0], res1[0][1], res1[0][2], res1[0][3], res2[0][0], res3[0][0], res3[0][1],
            res4[local_vars.stks][0], res4[local_vars.stks][1], res4[local_vars.stks][2], res4[local_vars.stks][3],
            res4[local_vars.stks][4], bstype, local_vars.cn, local_vars.cn, local_vars.osn, dates, dates, dates))
        local_vars.osn += 1
        local_vars.cn += 1
        # 判断是否为收益互换
        if is_swap == 'yes':
            datalist.append((
                local_vars.osn, res1_B[0][0], res1_B[0][1], res1_B[0][2], res1_B[0][3], res2_B[0][0], res3_B[0][0],
                res3_B[0][1], res4[local_vars.stks][0], res4[local_vars.stks][1], res4[local_vars.stks][2],
                res4[local_vars.stks][3], res4[local_vars.stks][4], bstype, local_vars.cn, local_vars.cn,
                local_vars.osn, dates, dates, dates))
            local_vars.osn += 1
            local_vars.cn += 1
        # if判断res4行数，如果stks小于res4行数，stks+1，否则stks=0
        if local_vars.stks < len(res4) - 1:
            local_vars.stks += 1
        else:
            local_vars.stks = 0


    startthread('openorder ', insert_openorder, datalist, threadnum, int(counts))



    print("openorder插入完成！")


def make_openorderdetail(productNum, productAcctNum, portfolioNum, bstype, exchid, counts, productNum_B=0,
                         productAcctNum_B=0, portfolioNum_B=0):
    global osn, sn, cn, stks, commit_cns, is_swap
    local_vars.osn = osn
    local_vars.sn = sn
    local_vars.cn = cn
    local_vars.stks = stks
    local_vars.commit_cns = commit_cns
    local_vars.is_swap = is_swap

    # Connect to MySQL database
    db = pymysql.connect(host=host, port=port, user=user, password=password, database=database,
                         charset="utf8")
    cursor = db.cursor()
    # 获取交易日期
    trade_date = "select tradedate from sysconfig;"
    cursor.execute(trade_date)
    trade_date = cursor.fetchone()
    dates = int(str(trade_date[0]) + '160330')
    # print("交易日：" + str(trade_date[0]))

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

    if is_swap == 'yes':
        cursor.execute(sql1, (productNum_B, productAcctNum_B, portfolioNum_B))
        res1_B = cursor.fetchall()
        cursor.execute(sql2, productAcctNum_B)
        res2_B = cursor.fetchall()
        cursor.execute(sql3, (productAcctNum_B, exchid))
        res3_B = cursor.fetchall()

    cursor.execute(sql4, exchid)
    res4 = cursor.fetchall()
    # print(res4[0][0], res4[0][1], res4[0][2], res4[0][3], res4[0][4])
    # print("===================================================")
    cursor.close()
    db.close()
    print("openorderdetail插入数据开始，请稍等...")

    insert_openorderdetail = (
        "INSERT INTO openorderdetail (OrigSerialNo, SerialNo, Source, Channel, productNum, productAcctNum, "
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

    datalist = []
    for local_vars.i in range(int(counts)):
        datalist.append((
            local_vars.osn, local_vars.sn, res1[0][0], res1[0][1], res1[0][2], res2[0][0], res3[0][0], res3[0][1],
            res4[local_vars.stks][0], res4[local_vars.stks][1], res4[local_vars.stks][2], res4[local_vars.stks][3], 
            res4[local_vars.stks][4], bstype, local_vars.cn, local_vars.cn, dates, dates, dates, 0))
        local_vars.osn += 1
        local_vars.sn += 1
        local_vars.cn += 1
        # 判断是否为收益互换
        if is_swap == 'yes':
            datalist.append((
                local_vars.osn, local_vars.sn, res1_B[0][0], res1_B[0][1], res1_B[0][2], res2_B[0][0], res3_B[0][0], res3_B[0][1],
                res4[local_vars.stks][0], res4[local_vars.stks][1], res4[local_vars.stks][2], res4[local_vars.stks][3], 
                res4[local_vars.stks][4], bstype, local_vars.cn, local_vars.cn, dates, dates, dates, local_vars.osn-1))
            local_vars.osn += 1
            local_vars.sn += 1
            local_vars.cn += 1
        # if判断result4行数，如果stks小于result4行数，stks+1，否则stks=0
        if local_vars.stks < len(res4) - 1:
            local_vars.stks += 1
        else:
            local_vars.stks = 0

    startthread('openorderdetail ', insert_openorderdetail, datalist, threadnum, int(counts))


    print("openorderdetail插入完成！")


def make_tradingresult(productNum, productAcctNum, portfolioNum, bstype, exchid, counts, productNum_B=0,
                       productAcctNum_B=0, portfolioNum_B=0):
    global osn, sn, cn, stks, commit_cns, is_swap
    local_vars.osn = osn
    local_vars.sn = sn
    local_vars.cn = cn
    local_vars.stks = stks
    local_vars.commit_cns = commit_cns
    local_vars.is_swap = is_swap

    # Connect to MySQL database
    db = pymysql.connect(host=host, port=port, user=user, password=password, database=database,
                         charset="utf8")
    cursor = db.cursor()
    # 获取交易日期
    trade_date = "select tradedate from sysconfig;"
    cursor.execute(trade_date)
    trade_date = cursor.fetchone()
    dates = int(str(trade_date[0]) + '160330')
    # print("交易日：" + str(trade_date[0]))

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

    if is_swap == 'yes':
        cursor.execute(sql1, (productNum_B, productAcctNum_B, portfolioNum_B))
        res1_B = cursor.fetchall()
        cursor.execute(sql2, productAcctNum_B)
        res2_B = cursor.fetchall()
        cursor.execute(sql3, (productAcctNum_B, exchid))
        res3_B = cursor.fetchall()

    cursor.execute(sql4, exchid)
    res4 = cursor.fetchall()
    # print(res4[0][0], res4[0][1], res4[0][2], res4[0][3], res4[0][4])
    # print("===================================================")
    cursor.close()
    db.close()
    print("tradingresult插入数据开始，请稍等...")

    insert_tradingresult = (
        "INSERT INTO tradingresult (OrigSerialNo, OrigSource, OrigChannel, SerialNo, productNum, "
        "productAcctNum, PortfolioNum, PortfolioName, acctid, exchId, regId, offerRegId, stkId, stkName, F_hedgeFlag, "
        "coveredFlag, stkType, tradeType, deskId, BsType, OCFlag, orderTypeFlag, orderTypeDetailFlag, ReportType, "
        "OrderFlag, knockQty, postQty, knockPrice, knockAmt, fullknockAmt, accuredInterest, knockCode, reckoningAmt, "
        "settleReckoningAmt, ThirdContractNo, ContractNum, openUsedMarginAmt, closePNL, OffsetMarginAmt, stampTax, "
        "tradetransFee, reckoningFee, transRuleFee, handlingFee, stkMngFee, exchtransFee, ventureFee, commision, "
        "otherFee, instDetailSerialNum, InstructId, basketId, BatchSerialNo, ThirdSystemId, NoOrderFlag, ExchRate, "
        "SequenceNo, targetDeskId, targetRegId, appointNo, occurTime, knockTime, postProcessFlag, exchProperty, "
        "totalCommision, F_MatchCondition, F_OrderPriceType, stopPrice, StkProperty, GwSequenceNo, IntelligentType, "
        "arbiContractID, MktOrderFlag, adjustRate, tdCloseQty) VALUES(%s, '3', '', %s, %s, %s, %s, "
        "%s, %s, '1', %s, %s, %s, %s, 'SPEC', %s, %s, %s, '', %s, 'O', "
        "'0', '00', '1', 'N', 100, 0, 11.4000, 1140.00, 1140.00, 0.00000000, %s, -1193.48, -1193.48, %s, %s, 0.00, "
        "0.00, 0.00, 1.14, 1.14, 1.14, 1.20, 1.14, 1.14, 1.14, 1.14, 50.00, 0.00, 0, '', '', %s, '2301', 'N', "
        "1.000000, 1, '', '', '', %s, %s, 0, '0', 53.48, '', 'LIMIT', 0.0000, '0', -1, 'DMA', '', '', 0.000000, 100);")

    datalist = []
    for local_vars.i in range(int(counts)):
        datalist.append((
            local_vars.osn, local_vars.sn, res1[0][0], res1[0][1], res1[0][2], res1[0][3], res2[0][0], res3[0][0],
            res3[0][1], res4[local_vars.stks][0], res4[local_vars.stks][1], res4[local_vars.stks][2], res4[local_vars.stks][3], 
            res4[local_vars.stks][4], bstype, local_vars.osn, local_vars.cn, local_vars.cn, local_vars.osn, dates, dates))
        local_vars.osn += 1
        local_vars.sn += 1
        local_vars.cn += 1
        # 判断是否为收益互换
        if is_swap == 'yes':
            datalist.append((
                local_vars.osn, local_vars.sn, res1_B[0][0], res1_B[0][1], res1_B[0][2], res1_B[0][3], res2_B[0][0], res3_B[0][0],
                res3_B[0][1], res4[local_vars.stks][0], res4[local_vars.stks][1], res4[local_vars.stks][2], res4[local_vars.stks][3], 
                res4[local_vars.stks][4], bstype, local_vars.osn-1, local_vars.cn, local_vars.cn, local_vars.osn, dates, dates))
            local_vars.osn += 1
            local_vars.sn += 1
            local_vars.cn += 1
        # if判断result4行数，如果stks小于result4行数，stks+1，否则stks=0
        if local_vars.stks < len(res4) - 1:
            local_vars.stks += 1
        else:
            local_vars.stks = 0

    startthread('tradingresult ', insert_tradingresult, datalist, threadnum, int(counts))

    print("tradingresult插入完成！")


if __name__ == '__main__':
    start_time = time.time()  # 记录方法开始时间

    Process1 = Process(target=make_openorder,
                       args=(
                       productNum, productAcctNum, portfolioNum, bstype, exchid, counts, productNum_B, productAcctNum_B,
                       portfolioNum_B))
    Process2 = Process(target=make_openorderdetail,
                       args=(
                       productNum, productAcctNum, portfolioNum, bstype, exchid, counts, productNum_B, productAcctNum_B,
                       portfolioNum_B))
    Process3 = Process(target=make_tradingresult,
                       args=(
                       productNum, productAcctNum, portfolioNum, bstype, exchid, counts, productNum_B, productAcctNum_B,
                       portfolioNum_B))
    # 启动线程
    Process1.start()
    Process2.start()
    Process3.start()
    # 等待线程完成
    Process1.join()
    Process2.join()
    Process3.join()

    end_time = time.time()  # 记录方法结束时间
    elapsed_time = end_time - start_time  # 计算耗时
    print(f"Elapsed time: {elapsed_time:.2f} seconds")
    print("All methods have finished.")
