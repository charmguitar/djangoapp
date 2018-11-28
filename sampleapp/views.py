import datetime
from django.shortcuts import redirect
from django.views import generic
from scalendar.forms import BS4ScheduleForm
from scalendar.views import MonthCalendarMixin, WeekCalendarMixin,WeekWithScheduleMixin


class MyCalendar(MonthCalendarMixin, WeekWithScheduleMixin, generic.CreateView):
    """月間カレンダー、週間カレンダー、スケジュール登録画面"""
    template_name = 'sampleapp/mycalendar.html'
    form_class = BS4ScheduleForm #scalendar/forms.pyでformの形を定義している。template内の{{ form }}に設置される。ここでpostしたデータを元に新規レコードがDBに自動で追加される?
    #{{ form.non_field_errors }}のように、多少プロパティをつけたformの作成も可能.もしかしたら、form_validの方で定義した方法でDBに格納されるかも.
    
    
    """
    
    templateに渡す値が、日付とスケジュールの対応が付けられたものになっているとよい。
    下記でそれを試している。get()の引数は式ではなく値である。
    この時点で、各日付（横軸）と時間（縦軸）とスケジュール（値）で対応づけられた配列のようなものがあるとよい。
    作成される表のマス数は7日*x(sec)分なので、一定。
    week.htmlでは、その分だけ回し、start_timeが一致するスケジュールがあるならば、そのマスで一回止まって設置するという流れ。
    
    縦:24時間*60分 = 1440 。30分毎にラインを引く。縦幅は一定。
    横：7つ。横幅は可変。
    
    年月日と分単位までの時刻が一致した場合、その予定をセル上に表示。セル内部ではなく、上辺をセルに合わせ、下辺はfloat状態にする。
    
    
    """
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['week'] = self.get_week_calendar() #templateで{{ week }} とすれば、この値となる.
        l = self.get_week_calendar()['schedule_list']
        print(l)
        for num in range(7):
            l.remove(num)
        print(l)        
        #print(l[1].get(date='2018-11-06'))

        context['month'] = self.get_month_calendar() #get_month_calendar()でインスタンスを生成して、templateに渡している.レコードの保存はしない。する場合は以下のformで定義している.
        list1 = list()
        for num in range(288):
            if (num % 12) == 0: #1時間毎に区切り線を入れる.5分間隔なので、あんまり正確ではない。
                t = num / 12 + 1
                if t <= 13:
                    list1.append('午前' + str(int(t)-1) + '時' )
                else:
                    list1.append('午後' + str(int(t)-13) + '時' )
            else:
                list1.append(num + 1)
        context['list1'] = list1   
        
        context['time'] = ['1時','2時','3時']
        return context

    def form_valid(self, form): #上記のform_class=BS4scheduleFormがエラーなく通った時、実行される。
        month = self.kwargs.get('month') #self.kwargsはurlに含まれる引数(id?).日付選択時にurlが変更され、引数も変わる.それを利用している.
        year = self.kwargs.get('year')
        day = self.kwargs.get('day')
        
        if month and year and day:
            date = datetime.date(year=int(year), month=int(month), day=int(day))
        else:
            date = datetime.date.today() #urlがデフォルトなままで、日付が含まれていない場合は、今日の日付けなので、date.today()。
        schedule = form.save(commit=False) #formで入力されたデータを入れる.
        schedule.date = date #その中のdateを選択している日付に変更.
        schedule.save() #DBに格納する.
        return redirect('sampleapp:mycalendar', year=date.year, month=date.month, day=date.day)

#これ以降は、個別に分けたカレンダーで使用していない.
"""
class MonthCalendar(MonthCalendarMixin, generic.TemplateView):
    #月間カレンダーを表示するビュー
    template_name = 'sampleapp/month.html'

    def get_context_data(self, **kwargs): #DBからデータを読み込む用
        context = super().get_context_data(**kwargs) #はじめに継承元のメソッドを呼び出す.たぶん、おまじないみたいなもの.
        context['month'] = self.get_month_calendar() #templateで{{ month }} とすれば、この値となる.
        return context


class WeekCalendar(WeekCalendarMixin, generic.TemplateView):
    #週間カレンダーを表示するビュー
    template_name = 'sampleapp/week.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['week'] = self.get_week_calendar()
        return context


class WeekWithScheduleCalendar(WeekWithScheduleMixin, generic.TemplateView):
    #スケジュール付きの週間カレンダーを表示するビュー
    template_name = 'sampleapp/week_with_schedule.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['week'] = self.get_week_calendar()
        return context


class MonthWithScheduleCalendar(MonthWithScheduleMixin, generic.TemplateView):
    #スケジュール付きの月間カレンダーを表示するビュー
    template_name = 'sampleapp/month_with_schedule.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['month'] = self.get_month_calendar()
        return context
"""


