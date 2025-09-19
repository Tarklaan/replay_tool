import plotly.graph_objects as go
import pandas as pd
import streamlit as st


def resample_data(df: pd.DataFrame, timeframe: str):
    if df is None or df.empty:
        return df
    
    df_copy = df.copy()
    df_copy["datetime"] = pd.to_datetime(df_copy["datetime"])
    df_copy.set_index("datetime", inplace=True)
    
    timeframe_map = {
        "1M": "1T",
        "5M": "5T", 
        "15M": "15T",
        "30M": "30T",
        "1H": "1H",
        "4H": "4H",
        "1D": "1D"
    }
    
    freq = timeframe_map.get(timeframe, "1T")
    
    resampled = df_copy.resample(freq).agg({
        'open': 'first',
        'high': 'max',
        'low': 'min',
        'close': 'last',
        'volume': 'sum'
    }).dropna()
    
    resampled.reset_index(inplace=True)
    
    if 'phase' in df.columns:
        phase_data = df.groupby(df['datetime'].dt.floor(freq))['phase'].first()
        phase_data.index.name = 'datetime'
        phase_df = phase_data.reset_index()
        resampled = resampled.merge(phase_df, on='datetime', how='left')
        resampled['phase'] = resampled['phase'].fillna('static')
    
    return resampled


def plot_candles(df: pd.DataFrame, title: str = "Candlestick Chart", height: int = 600):
    if df is None or df.empty:
        st.error("No data available to plot.")
        return

    df = df.copy()
    df["datetime"] = pd.to_datetime(df["datetime"])

    fig = go.Figure()
    
    fig.add_trace(
        go.Candlestick(
            x=df["datetime"],
            open=df["open"],
            high=df["high"],
            low=df["low"],
            close=df["close"],
            name="",
            showlegend=False,
            increasing_line_color='#26a69a',
            increasing_fillcolor='#26a69a',
            decreasing_line_color='#ef5350',
            decreasing_fillcolor='#ef5350',
            line=dict(width=1),
        )
    )

    fig.update_layout(
        title=dict(
            text=title,
            x=0.02,
            y=0.98,
            font=dict(size=18, color='white', family='Arial Black')
        ),
        xaxis=dict(
            title="",
            rangeslider=dict(visible=False),
            showgrid=True,
            gridcolor='rgba(128,128,128,0.1)',
            showspikes=True,
            spikecolor="rgba(255,255,255,0.6)",
            spikethickness=1,
            spikedash="solid",
            spikemode="across"
        ),
        yaxis=dict(
            title="",
            side="right",
            showgrid=True,
            gridcolor='rgba(128,128,128,0.1)',
            showspikes=True,
            spikecolor="rgba(255,255,255,0.6)",
            spikethickness=1,
            spikedash="solid",
            spikemode="across"
        ),
        height=height,
        plot_bgcolor='#0b0f1a',
        paper_bgcolor='#0b0f1a',
        font=dict(color='white', family='Arial'),
        margin=dict(l=0, r=80, t=50, b=30),
        hovermode='x unified',
        dragmode='pan',
        showlegend=False
    )
    
    fig.update_xaxes(
        showline=True,
        linewidth=1,
        linecolor='rgba(128,128,128,0.3)',
        mirror=False,
        tickfont=dict(size=11),
        fixedrange=False
    )
    
    fig.update_yaxes(
        showline=True,
        linewidth=1,
        linecolor='rgba(128,128,128,0.3)',
        mirror=False,
        tickfont=dict(size=11),
        fixedrange=False
    )

    chart_key = "main_chart"
    
    st.plotly_chart(
        fig, 
        use_container_width=True, 
        key=chart_key,
        config={
            'displayModeBar': True,
            'modeBarButtonsToAdd': ['drawline', 'drawrect', 'eraseshape'],
            'modeBarButtonsToRemove': ['lasso2d', 'select2d', 'autoScale2d'],
            'displaylogo': False,
            'scrollZoom': True,
            'doubleClick': 'autosize',
            'toImageButtonOptions': {
                'format': 'png',
                'filename': f'{title}_chart',
                'height': height,
                'width': 1400,
                'scale': 2
            }
        }
    )


def plot_replay_candles(static_df: pd.DataFrame, replay_df: pd.DataFrame, replay_index: int, title: str = "Replay Chart", height: int = 600):
    if static_df is None or static_df.empty:
        st.warning("⚠️ No static data available to plot.")
        return
    
    if replay_df is None or replay_df.empty:
        st.warning("⚠️ No replay data available.")
        return

    static_df["datetime"] = pd.to_datetime(static_df["datetime"])
    replay_df["datetime"] = pd.to_datetime(replay_df["datetime"])
    
    current_replay = replay_df.iloc[:replay_index + 1] if replay_index < len(replay_df) else replay_df

    fig = go.Figure()

    fig.add_trace(
        go.Candlestick(
            x=static_df["datetime"],
            open=static_df["open"],
            high=static_df["high"],
            low=static_df["low"],
            close=static_df["close"],
            name="Static",
            opacity=0.7,
        )
    )

    if not current_replay.empty:
        fig.add_trace(
            go.Candlestick(
                x=current_replay["datetime"],
                open=current_replay["open"],
                high=current_replay["high"],
                low=current_replay["low"],
                close=current_replay["close"],
                name="Replay",
                increasing_line_color="lime",
                decreasing_line_color="red",
            )
        )

    fig.update_layout(
        title=title,
        xaxis=dict(title="Time", rangeslider=dict(visible=False)),
        yaxis=dict(title="Price"),
        height=height,
        template="plotly_dark",
        margin=dict(l=20, r=20, t=40, b=20),
    )

    st.plotly_chart(fig, use_container_width=True, key=f"replay_chart_{replay_index}_{hash(str(current_replay.iloc[-1]['datetime']) if len(current_replay) > 0 else 'empty')}")