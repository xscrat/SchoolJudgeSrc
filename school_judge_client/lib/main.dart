import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'choose_judge.dart';
import 'judge_mark.dart';

void main() {
  WidgetsFlutterBinding.ensureInitialized();
  SystemChrome.setPreferredOrientations([DeviceOrientation.portraitUp])
      .then((_) {
    runApp(new MyApp());
  });
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: '',
      routes: <String, WidgetBuilder>{
        JudgeMarkStatefulWidget.routeName: (BuildContext context) =>
            new JudgeMarkStatefulWidget(title: ''),
      },
      home: new Scaffold(
        backgroundColor: Colors.white,
        appBar: new AppBar(
          title: new Text(''),
        ),
        body: new Center(
          child: new ChooseJudgeStatefulWidget(),
        ),
      ),
    );
  }
}
