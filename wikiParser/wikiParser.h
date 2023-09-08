#pragma once

#include <QtWidgets>
#include "ui_wikiParser.h"

class wikiParser : public QMainWindow
{
    Q_OBJECT

public:
    wikiParser(QWidget *parent = nullptr);
    ~wikiParser();

private:
    Ui::wikiParserClass ui;
};
