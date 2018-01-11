package kr.ac.cnu.counteruav;

import android.content.Context;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.BaseAdapter;
import android.widget.ListView;
import android.widget.TextView;

import java.util.ArrayList;

/**
 * Created by hwangtaewook on 18. 1. 11.
 */

public class radarItemAdapter extends BaseAdapter{
    Context context;
    ArrayList<radarItem> radarItems;

    public radarItemAdapter(Context context, ArrayList<radarItem> radarItems) {
        this.context = context;
        this.radarItems = radarItems;
    }

    @Override
    public int getCount() {
        return this.radarItems.size();
    }

    @Override
    public Object getItem(int position) {
        return radarItems.get(position);
    }

    @Override
    public long getItemId(int position) {
        return position;
    }

    @Override
    public View getView(int position, View convertView, ViewGroup parent) {
        if (convertView == null) {
            convertView = LayoutInflater.from(context).inflate(R.layout.radar_item, null);

            ((TextView)convertView.findViewById(R.id.radar_name)).setText(radarItems.get(position).getRadarName());
        }

        return convertView;
    }
}
