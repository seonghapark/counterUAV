package com.example.root.subzmq1;

import android.os.Bundle;
import android.os.Handler;
import android.os.Message;
import android.support.v7.app.AppCompatActivity;
import android.util.Log;

import com.github.mikephil.charting.charts.LineChart;
import com.github.mikephil.charting.components.XAxis;
import com.github.mikephil.charting.data.Entry;
import com.github.mikephil.charting.data.LineData;
import com.github.mikephil.charting.data.LineDataSet;
import com.github.mikephil.charting.interfaces.datasets.ILineDataSet;
import com.github.mikephil.charting.utils.ColorTemplate;

import org.zeromq.ZMQ;

import java.util.ArrayList;
import java.util.List;

public class ChartActivity extends AppCompatActivity {

    TestHandler handler;
    int length;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_chart);

        length = 25;

        handler = new TestHandler();


        Thread thread1 = new Thread(new Runnable() {
            @Override
            public void run() {

                ZMQ.Context context = ZMQ.context(1);
                ZMQ.Socket socket = context.socket(ZMQ.SUB);
                socket.subscribe("".getBytes());
                socket.connect("tcp://127.0.0.1:5559");

                while(!Thread.currentThread().isInterrupted()) {
                    String recvTimes = new String(socket.recv());
                    String recvDistances = new String(socket.recv());
                    try {
                        handler.setTimes(recvTimes);
                        handler.setDistances(recvDistances);
                        Message msg = handler.obtainMessage();
                        handler.sendMessage(msg);
                    } catch (Exception ex) {
                        Log.e("ChartActivity", "Exception in processing message.", ex);
                    }
                }
                socket.close();
                context.term();
                System.out.println("end!");

            }
        });
        thread1.start();
    }

    public class TestHandler extends Handler {
        List<Integer> colors;
        LineChart lineChart;
        ArrayList<ILineDataSet> lineDataSets;
        ArrayList<Entry> lineEntries;

        String times, distances;

        int second;

        public TestHandler() {
            colors = new ArrayList<Integer>();
            for (int c : ColorTemplate.PASTEL_COLORS)
                colors.add(c);

            lineChart = (LineChart) findViewById(R.id.lineChart);
            lineDataSets = new ArrayList<ILineDataSet>();
            lineEntries = new ArrayList<Entry>();

            second = 0;
        }

        private void setTimes(String times) {
            this.times = times;
        }
        private void setDistances(String distances) {
            this.distances = distances;
        }

        public void handleMessage(Message msg) {

            String[] timesOfSec = times.split(" ");
            String[] distancesOfSec = distances.split(" ");

            for (int i=0; i<timesOfSec.length; i++) {
                lineEntries.add(new Entry(Float.parseFloat(timesOfSec[i]), Float.parseFloat(distancesOfSec[i])));
            }
            LineDataSet lineDataSet = new LineDataSet(lineEntries, "testData");
            lineDataSet.setColor(colors.get(0));
            lineDataSet.setDrawCircles(false);

            lineDataSets.add(lineDataSet);
            LineData lineData = new LineData(lineDataSets);
            lineChart.setData(lineData);
            XAxis xAxis = lineChart.getXAxis();
            xAxis.setAxisMinimum(-24+second);

            lineChart.setVisibleXRange(0, length);lineChart.getDescription().setText("");
//            lineChart.setVisibleYRange(0, 70, YAxis.AxisDependency.LEFT);

            lineChart.invalidate();

            second++;
        }
    }
}