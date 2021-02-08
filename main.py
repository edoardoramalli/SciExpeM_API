from API import *
from django.db.models import Q
from datetime import datetime
from Models import ChemModel


def main():
    # prova(verbose=True)
    # exit()

    # ----- Get User Info -----
    # response = getUserInfo("root", "Milano.2020")
    # print(response['token'])

    # ----- Insert Model -----
    model_name = 'POLIMI_1006_H2'
    kinetics = open("/Users/edoardo/Dropbox/SciExpem/OpenSmoke++/Modelli/H2/" + model_name + "/kinetics/kinetics.xml").read()
    reactions = open(
        "/Users/edoardo/Dropbox/SciExpem/OpenSmoke++/Modelli/H2/" + model_name + "/kinetics/reaction_names.xml").read()

    m1 = ChemModel(name=model_name,
                   xml_file_kinetics=kinetics,
                   xml_file_reaction_names=reactions)

    insertChemModel(m1, verbose=True)

    # ----- Get Model List -----
    models = filterChemModel(name=model_name)
    model_0 = models[0]
    print("Model Name:", model_0.name)


    # ----- Get Experiment List -----
    experiments = filterExperiment(fileDOI__contains='g00000001_x')
    exp_0 = experiments[0]
    print("Experiment Status:", exp_0.status)
    # print(exp_0.os_input_file)

    # ----- Add OS File -----
    # osFile_string = open("/Users/edoardo/Dropbox/SciExpem/OpenSmoke++/Simulazioni/CRECK_1412/H2_indirect_v2_0_preliminary/g00000001_x.xml.dic").read()
    # insertOSFile(exp_0, osFile_string, verbose=True)

    # ----- Verify Experiment -----
    # verifyExperiment(experiment=exp_0, status='verified', verbose=True)

    # ----- Start Simulation -----
    startSimulation(experiment=exp_0, chemModel=model_0, verbose=True)

    # ----- Filter Execution -----
    exec = filterExecution(experiment_id=exp_0.id)
    print(exec)
    # print(exec.execution_start)
    # print(exec.execution_end)
    # print(exec.execution_columns_df)
    # print(exec.execution_columns_units)

    # ----- Execute Curve Matching Base -----
    x = [1,2,3,4,5]
    y = [1, 2, 3, 4, 5]
    for execution in exec:
        analyzeExecution(execution)

    # ----- Filter CurveMatchingResult -----
    cm_result = filterCurveMatchingResult(execution_column__execution__experiment__id=exp_0.id)
    for cm in cm_result:
        print("CM: ", cm.index)
    # print(cm_result)
    # prova()





    # print(exp_0.experimentClassifier)
    # print(dir(exp_0))
    # print(len(experiment))
    # for r in result:
    #     print(r.fileDOI)
    #     # txt = create_header(r, r.FilePaper)
    #     # txt = create_common_experimental_conditions(r.InitialSpecie)
    #     # print(r.DataColumn)
    #     # dg1 = []
    #     # dg2 = []
    #     # for column in r.DataColumn:
    #     #     if column.dg_id == "dg1":
    #     #         dg1.append(column)
    #     #     elif column.dg_id == "dg2":
    #     #         dg2.append(column)
    #     txt = create_RCM(r, r.DataColumn, r.InitialSpecie, r.CommonProperty, r.FilePaper)
    #     a = executeOptimaPP(file=txt)
    #     for l in a:
    #         print(l, end="")
    #     print(txt)
    #     break
    #

    # print(len(result)
    # # #
    # # result2 = filterExperiment(Q(reactor="shock tube") | Q(reactor="flow reactor"))
    # # print(len(result2))
    #
    # paper = FilePaper("Titolo", "g0002")
    # property1 = CommonProperty("P0", "atm", "5")
    # data1 = DataColumn("IDT", "ms", [0.001, 0.005], "01")
    # data2 = DataColumn("T0", "K", [0.002, 0.006], "01")
    # init1 = InitialSpecie("H2O", "mole", "0.98")
    # init2 = InitialSpecie("O2", "mole", "0.48")
    # exp = Experiment("Shock Tube", "IDT", "G002", paper, [data1, data2], [init1, init2], [property1])
    #
    # exe_data1 = ExecutionColumn([1, 2, 3, 4, 5], "ms", "t", "IDT")
    # exe_data2 = ExecutionColumn([11, 22, 33, 44, 55], "K", "t", "IDT")
    #
    # exec = Execution(H2_2003, exp, [exe_data1, exe_data2])
    #
    # insertExecution(exec, True)

    # m = filterChemModel(name="ModelEdo2")[0]
    # print(m.xml_file_kinetics)

    # e = filterExecution(chemModel__name="ModelEdo2", experiment__fileDOI="G002")[0]
    # print(e.ExecutionColumn[0].id)
    #
    # # cm = CurveMatchingResult(e.ExecutionColumn[0], 0.5, 0.3)
    #
    # r = filterCurveMatchingResult(execution_column__id=1)[0]
    # print(r.index, r.error)
    # print(r.execution_column.execution.experiment.data_columns_df)

    # print("Begin Time =", datetime.now().strftime("%H:%M:%S"))
    # l = filterChemModel(time="edp")
    # print("End Time =", datetime.now().strftime("%H:%M:%S"))
    # for e in l:
    #     print(e.name)

    # x_exp = [6, 7, 8, 9, 10]
    # y_exp = [6, 7, 8, 9, 10]
    # x_sim = [1, 2, 3, 4, 5]
    # y_sim = [1, 2, 3, 4, 5]
    #
    # error, index = executeCurveMatchingBase(x_exp=x_exp, y_exp=y_exp, x_sim=x_sim, y_sim=y_sim)
    # print(error, index)
    # #
    # f = open("./tmp/RCMExample", "r")
    # f = f.read()
    # a = executeOptimaPP(file=f)
    #
    # print(a)

    # a = executeCurveMatchingBase(file=f)
    # f = ""
    # for l in a:
    #     f += l
    #
    # reac_file = open("file.xml", "w+")
    # reac_file.write(f)
    # reac_file.close()

    # path = "file.xml"
    #

    # path = "/Users/edoardo/Dropbox/SciExpem/OpenSmoke++/Simulazioni/Respecth_H2/g00000001_x.xml"
    # loadXMLExperiment(path, verbose=True)
    # path = "./tmp/JSRExample.xml"
    # path = "./tmp/RCMExample.xml"
    # path = "./tmp/outletConcentrationExample.xml" OK
    # path = "./tmp/laminarFlameExample.xml" OK
    # path = "./tmp/directRateDeterminationExample.xml"
    # path = "./tmp/concentrationProfileExample.xml"
    # loadXMLExperiment(path, verbose=True)

    # import glob
    # files = glob.glob("/Users/edoardo/Desktop/Esperimenti/syngas_indirect_v2_0_preliminary/*.xml")
    # print(len(files))
    # error = 0
    # for f in files:
    #     print(f)
    #     try:
    #         loadXMLExperiment(f, verbose=True)
    #         print()
    #     except Exception as e:
    #         print(e)
    #         error += 1
    #         # input("GO!")
    # print(error)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
