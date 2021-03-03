import 'package:flutter/material.dart';
import 'dart:convert';
import 'judge_mark.dart';
import 'package:http/http.dart' as http;
import 'globals.dart' as globals;

class ChooseJudgeStatefulWidget extends StatefulWidget {
  @override
  createState() => new ChooseJudgeState();
}

class ChooseJudgeState extends State<ChooseJudgeStatefulWidget> {
  int choosenIndex = -1;
  List<String> allJudgeNames = [];

  @override
  void initState() {
    http
        .get(
            'http://${globals.serverIP}:${globals.serverPort}/get_judge_names/')
        .then((response) {
      if (response.statusCode == 200) {
        var judgeNames = json.decode(response.body)['judge_names'];
        for (var i = 0; i < judgeNames.length; i++) {
          allJudgeNames.add(judgeNames[i]);
        }
        setState(() {});
      }
    });
    super.initState();
  }

  @override
  Widget build(BuildContext context) {
    final size = MediaQuery.of(context).size;
    return new Column(
      children: <Widget>[
        Expanded(
          flex: 1,
          child: Center(
            child: Text(
              '评委列表',
              textAlign: TextAlign.center,
              style: TextStyle(fontSize: 25),
            ),
          ),
        ),
        Expanded(
          flex: 8,
          child: Container(
            child: ListView.builder(
                itemCount: allJudgeNames.length,
                itemBuilder: (context, i) {
                  return new Container(
                    decoration: new BoxDecoration(
                      color: choosenIndex == i
                          ? Colors.lightGreen
                          : Color(0x000000),
                    ),
                    child: new ListTile(
                      title: new Text(
                        allJudgeNames[i],
                        textAlign: TextAlign.center,
                        style: TextStyle(fontSize: 20),
                      ),
                      onTap: () {
                        setState(() {
                          choosenIndex = i;
                        });
                      },
                    ),
                  );
                }),
          ),
        ),
        Expanded(
          flex: 1,
          child: Center(
            child: RaisedButton(
              child: Text(
                '进入节目打分页面',
                textAlign: TextAlign.center,
                style: TextStyle(fontSize: 30),
              ),
              onPressed: () {
                if (choosenIndex == -1) {
                  showDialog(
                    context: context,
                    child: new AlertDialog(
                      title: new Text('请先选择评委', textAlign: TextAlign.center),
                    ),
                  );
                } else {
                  http
                      .post(
                          'http://${globals.serverIP}:${globals.serverPort}/post_judge_register/$choosenIndex/')
                      .then((response) {
                    if (response.statusCode == 200) {
                      Navigator.pushNamed(
                          context, JudgeMarkStatefulWidget.routeName,
                          arguments: <String, int>{
                            'no': choosenIndex,
                          });
                    } else {
                      Widget cancelButton = FlatButton(
                        child: Text('取消'),
                        onPressed: () {
                          Navigator.of(context, rootNavigator: true).pop('dialog');
                        },
                      );
                      Widget enterButton = FlatButton(
                        child: Text('强制进入'),
                        onPressed: () {
                          Navigator.of(context, rootNavigator: true).pop('dialog');
                          Navigator.pushNamed(
                              context, JudgeMarkStatefulWidget.routeName,
                              arguments: <String, int>{
                                'no': choosenIndex,
                              });
                        },
                      );
                      showDialog(
                        context: context,
                        child: new AlertDialog(
                          title: new Text('已有他人选择此评委，强制进入打分页面吗？',
                              textAlign: TextAlign.center),
                          actions: [
                            cancelButton,
                            enterButton,
                          ],
                        ),
                      );
                    }
                  });
                }
              },
            ),
          ),
        ),
      ],
    );
  }
}
