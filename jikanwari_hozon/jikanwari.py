import openpyxl
from datetime import datetime, date, timedelta
import calendar
import pandas as pd
from dateutil.relativedelta import relativedelta
import excel2img
import os

#時間割の区切り月月日を取得する関数群
class jikanwari_datetime:
  def __init__(self):
    self._wd_list = ['mon', 'tue', 'wed', 'thu', 'fry', 'sat', 'sun'] 
  
  #週の指定された曜日の日付取得
  def first_wd_date(self, dt, first_wd = 'sun'):
    wd = self._wd_list.index(first_wd)
    if dt.weekday() == wd:
      first_wd_dt = dt
    elif dt.weekday() > wd:
      first_wd_dt = dt - timedelta(days=dt.weekday()) + timedelta(days=wd)
    elif dt.weekday() < wd:
      first_wd_dt = dt + timedelta(days=wd - dt.weekday() -7)
    return first_wd_dt
  
  #年度取得
  def school_year(self, dt):
    y = dt.year
    if dt.month <= 3:
        sy = y-1 
    else:
        sy = y
    return sy
  
  #月の最初の日付取得
  def first_date(self, dt):
    m = dt.month
    y = dt.year
    return date(y, m, 1)

  #月の最終日取得
  def last_date(self, dt):
    m = dt.month
    y = dt.year
    last_day = calendar.monthrange(y, m)[1]
    return date(y, m, last_day)


#時間割を画像化クラス作成
class make_gazou(jikanwari_datetime):
  #sy:年度, first_row:エクセルファイルの時間割開始行, 
  #w_nrow:各週の時間割に使用する行数, first_wd:時間割の始まりの曜日(def=日曜日)
  #first_col,last_col:時間割の始まりと終わりの列を引数
  def __init__(self, sy, first_row, w_nrow, first_col, last_col, first_wd = 'sun'):
    self._wd_list = ['mon', 'tue', 'wed', 'thu', 'fry', 'sat', 'sun'] 
    self.sy = sy
    self.first_row = first_row
    self.w_nrow = w_nrow
    self.first_wd = first_wd

    #年度の始まり（4月1日）取得
    self._Apr1 = date(self.sy, 4, 1)
    
    #4月1日の週のfirst_weekdayを取得
    self._jikanwari_first_dt = self.first_wd_date(self._Apr1, self.first_wd)

    #Excelファイルのセル番号と日付の対応表作成
    wd_dt = self._jikanwari_first_dt
    wd_dts = []
    first_cells = []
    last_cells = []
    row = self.first_row
    first_cell = first_col + str(row)
    last_cell = last_col + str(row)
    for i in range(55):
        i
        wd_dts.append(wd_dt)
        first_cells.append(first_cell)
        last_cells.append(last_cell)
        wd_dt = wd_dt + timedelta(days=7)
        row = row + self.w_nrow
        first_cell = first_col + str(row)
        last_cell = last_col + str(row + (self.w_nrow - 1))
    self._excel_col_ref = pd.DataFrame({"date" : wd_dts, "first_cell" : first_cells, 
    "last_cell" : last_cells})

  #一ヶ月ver
  def make_gazou_month(self, dt, excel_path, png_dir, sheet_name = '時間割'):
    this_month = dt.month
    
    #エクセル範囲指定（一ヶ月）
    #月の開始
    first_dt = self.first_date(dt)
    first_calendar_dt = self.first_wd_date(first_dt, self.first_wd)
    first_cell_ref = self._excel_col_ref[self._excel_col_ref['date'] == first_calendar_dt] #対応表からセル番号取得
    first_cell = first_cell_ref['first_cell'].values[0]
    #月の終わり
    last_dt = self.last_date(dt)
    last_calendar_dt = self.first_wd_date(last_dt, self.first_wd) #カレンダー最終週の日曜日
    last_cell_ref = self._excel_col_ref[self._excel_col_ref['date'] == last_calendar_dt] #対応表から行取得
    last_cell = last_cell_ref['last_cell'] .values[0]
    range = first_cell + ':' + last_cell

    #3.Excel画像化
    png_path = png_dir + '/%s.png' %this_month
    excel2img.export_img(excel_path, png_path, sheet_name, "%s" %range)
    print("画像化に成功しました")