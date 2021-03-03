import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'globals.dart' as globals;
import 'judge_summary.dart';

class JudgeMarkStatefulWidget extends StatefulWidget {
  JudgeMarkStatefulWidget({Key key, this.title}) : super(key: key);

  static const String routeName = "/JudgeMark";

  final String title;

  @override
  _JudgeMarkStatefulWidgetState createState() =>
      _JudgeMarkStatefulWidgetState();
}

class _JudgeMarkStatefulWidgetState extends State<JudgeMarkStatefulWidget> {
  List<TextEditingController> _controllers = [];
  List<String> allProgramsNames = [];
  List<int> allProgramsIds = [];
  final _alreadySubmitPrograms = new Set<int>();

  @override
  void initState() {
    http
        .get("http://${globals.serverIP}:${globals.serverPort}/get_programs/")
        .then((response) {
      if (response.statusCode == 200) {
        var programsNames = json.decode(response.body)['programs_names'];
        var programsIds = json.decode(response.body)['programs_ids'];
        for (var i = 0; i < programsNames.length; i++) {
          allProgramsNames.add(programsNames[i]);
          allProgramsIds.add(programsIds[i]);
          _controllers.add(TextEditingController());
        }
        setState(() {});
      }
    });
    super.initState();
  }

  @override
  Widget build(BuildContext context) {
    final size = MediaQuery.of(context).size;
    final widgetPassInArgs =
        ModalRoute.of(context).settings.arguments as Map<String, int>;
    return new WillPopScope(
      onWillPop: () async => true,
      child: Scaffold(
        backgroundColor: Colors.white,
        appBar: AppBar(
          title: Text(widget.title),
        ),
        body: Center(
          child: Column(
            children: <Widget>[
              Expanded(
                flex: 9,
                child: Container(
                  child: ListView.builder(
                      itemCount: allProgramsNames.length,
                      itemBuilder: (context, i) {
                        return new Container(
                            color: _alreadySubmitPrograms
                                    .contains(allProgramsIds[i])
                                ? Colors.lightGreen
                                : Color(0x000000),
                            child: Row(
                                crossAxisAlignment: CrossAxisAlignment.center,
                                children: <Widget>[
                                  Expanded(
                                    flex: 4,
                                    child: Container(
                                      alignment: Alignment.center,
                                      margin: EdgeInsets.all(10),
                                      child: Text(
                                        '节目 ${allProgramsIds[i] + 1} 《${allProgramsNames[i]}》',
                                        style: TextStyle(fontSize: 20),
                                      ),
                                    ),
                                  ),
                                  Expanded(
                                    flex: 2,
                                    child: Container(
                                      alignment: Alignment.center,
                                      child: TextField(
                                        controller: _controllers[i],
                                        decoration:
                                            new InputDecoration.collapsed(
                                          hintText:
                                              '${widgetPassInArgs['no'] + 1}号评委请打分',
                                          hintStyle: TextStyle(
                                            fontSize: 20.0,
                                            color: Colors.grey,
                                          ),
                                        ),
                                        keyboardType: TextInputType.number,
                                        inputFormatters: [
                                          WhitelistingTextInputFormatter
                                              .digitsOnly
                                        ],
                                        textAlign: TextAlign.center,
                                        style: TextStyle(
                                          fontSize: 20.0,
                                          color: Colors.black,
                                        ),
                                      ),
                                    ),
                                  ),
                                  Expanded(
                                    flex: 2,
                                    child: Container(
                                        alignment: Alignment.center,
                                        child: FlatButton(
                                          child: new Text('提交',
                                              style: TextStyle(fontSize: 20)),
                                          color: Colors.orangeAccent,
                                          onPressed: () {
                                            http
                                                .post(
                                                    'http://${globals.serverIP}:${globals.serverPort}/post_mark/${widgetPassInArgs['no']}/${allProgramsIds[i]}/${_controllers[i].text}/')
                                                .then((response) {
                                              if (response.statusCode == 200) {
                                                showDialog(
                                                  context: context,
                                                  child: new AlertDialog(
                                                    title: new Text('提交成功',
                                                        textAlign:
                                                            TextAlign.center),
                                                  ),
                                                );
                                                setState(() {
                                                  _alreadySubmitPrograms
                                                      .add(allProgramsIds[i]);
                                                });
                                              } else {
                                                showDialog(
                                                  context: context,
                                                  child: new AlertDialog(
                                                    title: new Text('提交失败',
                                                        textAlign:
                                                            TextAlign.center),
                                                  ),
                                                );
                                              }
                                            });
                                          },
                                        )),
                                  ),
                                ]));
                      }),
                ),
              ),
              Expanded(
                  flex: 1,
                  child: Center(
                    child: RaisedButton(
                        child: Text('打分结束', style: TextStyle(fontSize: 30)),
                        onPressed: () {
                          Navigator.of(context).push(MaterialPageRoute(
                              builder: (context) => JudgeSummaryWidget()));
                        }),
                  )),
            ],
          ),
        ),
      ),
    );
  }
}
