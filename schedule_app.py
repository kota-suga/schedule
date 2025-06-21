from flask import Flask, render_template, request, send_from_directory
from datetime import datetime, timedelta
import os

# このファイル(app.py)のあるディレクトリを基準に static と templates フォルダを指定
base_dir = os.path.dirname(os.path.abspath(__file__))

app = Flask(
    __name__,
    template_folder=os.path.join(base_dir, "templates"),  # ← 明示的にテンプレートフォルダを指定
    static_folder=os.path.join(base_dir, "static"),
    static_url_path="/static"
)

@app.route("/")
def home():
    return render_template("home1.html")

@app.route("/submit", methods=["POST"])
def submit():
    technical_meeting = request.form.get("technical_meeting")
    design_document = request.form.get("design_document")
    specification_document = request.form.get("specification_document")
    all_ingredients = request.form.get("all_ingredients")
    annual_classification = request.form.get("annual_classification")
    prototype = request.form.get("prototype", "").strip()  # ← stripを追加
    response_date = request.form.get("response_date")
    trial_date = request.form.get("trial_date")

    schedule = [
        ("技打", technical_meeting),
        ("設計書", design_document),
        ("仕様書", specification_document),
        ("全成分", all_ingredients),
    ]
    if response_date:
        schedule.append(("回答時期", response_date))
    if trial_date:
        schedule.append(("試作", trial_date))

    # フォームデータを取得
    technical_meeting = request.form["technical_meeting"]  # 技打日
    design_document = request.form["design_document"]  # 設計書日
    specification_document = request.form["specification_document"]  # 仕様書日
    all_ingredients = request.form["all_ingredients"]  # 全成分日
    annual_classification = request.form["annual_classification"]  # 年次分類
    prototype = request.form["prototype"]  # 試作の有無

    print("受け取った年次分類:", repr(annual_classification))
    print("受け取った試作:", repr(prototype))
    
    trial_date_input = request.form.get("trial_date")  # 試作日程 (任意入力)
    result = request.form.get("result", "")
    response_date = None 
    response_date_str = request.form.get("response_date", "")

    if isinstance(response_date_str, str) and response_date_str.strip() != "":
        try:
            response_date = datetime.strptime(response_date_str, "%Y-%m-%d").date()
        except ValueError:
            response_date = None  # 万が一フォーマットが変でもエラーにしない

    # 日付を変換
    technical_meeting_date = datetime.strptime(technical_meeting, "%Y-%m-%d").date()
    design_document_date = datetime.strptime(design_document, "%Y-%m-%d").date()
    specification_document_date = datetime.strptime(specification_document, "%Y-%m-%d").date()
    all_ingredients_date = datetime.strptime(all_ingredients, "%Y-%m-%d").date()
    trial_date = None

    # 試作日程を取得 (試作ありの場合)
    if prototype == "with_prototype":
        if trial_date_input:
            trial_date = datetime.strptime(trial_date_input, "%Y-%m-%d").date()
        else:
            trial_date = "未定"


    # SPF測定あり、試作あり
    if annual_classification == "spf_with_test" and prototype == "with_prototype":
        schedule = [
            {"name": "技打", "date": technical_meeting_date},
            {"name": "設計書", "date": design_document_date},
            {"name": "仕様書", "date": specification_document_date},
            {"name": "全成分", "date": all_ingredients_date},
            {"name": "機能性ユニットへの連絡", "date": technical_meeting_date}, 
            {"name": "ソフト成分、美容剤、訴求内容の確認", "date": technical_meeting_date}, 
            {"name": "製品符号を立ててもらう", "date": technical_meeting_date}, 
            {"name": "チェックリストの送付", "date": design_document_date - timedelta(days=5)}, 
            {"name": "試作日程の確保", "date": design_document_date - timedelta(days=5)},
            {"name": "要注意特許の確認", "date": design_document_date + timedelta(days=1)},
            {"name": "設計書後対応", "date": design_document_date},
            {"name": "美容剤、ソフト成分再確認", "date": design_document_date},
            {"name": "美容剤検討依頼書が届いているか確認", "date": design_document_date+ timedelta(days=10)},
            {"name": "安定性の設置", "date": design_document_date},
            {"name": "ベース、色決定", "date": specification_document_date - timedelta(days=7)},
            {"name": "読み合わせ", "date": specification_document_date - timedelta(days=7)},
            {"name": "チェックリストの送付", "date": specification_document_date - timedelta(days=7)},
            {"name": "マスタ統合入力", "date": specification_document_date - timedelta(days=7)},
            {"name": "美容剤決定報告書", "date": specification_document_date - timedelta(days=7)},
            {"name": "スケールアップの計量依頼枠確保", "date": specification_document_date - timedelta(days=7)},
            {"name": "特許確定", "date": specification_document_date + timedelta(days=14)},
            {"name": "製品情報プロファイルの処方の登録", "date": specification_document_date},
            {"name": "香料ランクC以上確認", "date": specification_document_date},
            {"name": "安定性、安全性、防腐確認", "date": specification_document_date},
            {"name": "美容剤確認表の返送", "date": specification_document_date + timedelta(days=7)},
            {"name": "試作充填依頼メールの送付", "date": trial_date - timedelta(days=42)},
            {"name": "試作願の提出", "date": trial_date - timedelta(days=30)},
            {"name": "スケールアップ", "date": trial_date - timedelta(days=35)},
            {"name": "製品技術概要", "date": trial_date - timedelta(days=14)},
            {"name": "試作見本品の送付", "date": trial_date - timedelta(days=7)},
            {"name": "事前打ち合わせ", "date": trial_date - timedelta(days=7)},
        ]
        if response_date:
            schedule.append({"name": "SPFバルク提出", "date": response_date - timedelta(days=150)})

    # SPF測定あり、試作なし
    elif annual_classification == "spf_with_test" and prototype == "no_prototype":
        schedule = [
            {"name": "技打", "date": technical_meeting_date},
            {"name": "設計書", "date": design_document_date},
            {"name": "仕様書", "date": specification_document_date},
            {"name": "全成分", "date": all_ingredients_date},
            {"name": "機能性ユニットへの連絡", "date": technical_meeting_date}, 
            {"name": "ソフト成分、美容剤、訴求内容の確認", "date": technical_meeting_date}, 
            {"name": "製品符号を立ててもらう", "date": technical_meeting_date}, 
            {"name": "チェックリストの送付", "date": design_document_date - timedelta(days=5)}, 
            {"name": "要注意特許の確認", "date": design_document_date + timedelta(days=1)},
            {"name": "設計書後対応", "date": design_document_date},
            {"name": "美容剤、ソフト成分再確認", "date": design_document_date},
            {"name": "美容剤検討依頼書が届いているか確認", "date": design_document_date+ timedelta(days=10)},
            {"name": "安定性の設置", "date": design_document_date},
            {"name": "ベース、色決定", "date": specification_document_date - timedelta(days=7)},
            {"name": "読み合わせ", "date": specification_document_date - timedelta(days=7)},
            {"name": "チェックリストの送付", "date": specification_document_date - timedelta(days=7)},
            {"name": "マスタ統合入力", "date": specification_document_date - timedelta(days=7)},
            {"name": "美容剤決定報告書", "date": specification_document_date - timedelta(days=7)},
            {"name": "スケールアップの計量依頼枠確保", "date": specification_document_date - timedelta(days=7)},
            {"name": "特許確定", "date": specification_document_date + timedelta(days=14)},
            {"name": "製品情報プロファイルの処方の登録", "date": specification_document_date},
            {"name": "香料ランクC以上確認", "date": specification_document_date},
            {"name": "安定性、安全性、防腐確認", "date": specification_document_date},
            {"name": "美容剤確認表の返送", "date": specification_document_date + timedelta(days=7)},
        ]
    if response_date:
        schedule.append({"name": "SPFバルク提出", "date": response_date - timedelta(days=150)})
    
    # SPF測定なし、試作あり
    elif annual_classification == "no_spf" and prototype == "with_prototype":
        schedule = [
            {"name": "技打", "date": technical_meeting_date},
            {"name": "設計書", "date": design_document_date},
            {"name": "仕様書", "date": specification_document_date},
            {"name": "全成分", "date": all_ingredients_date},
            {"name": "ソフト成分、美容剤、訴求内容の確認", "date": technical_meeting_date}, 
            {"name": "製品符号を立ててもらう", "date": technical_meeting_date}, 
            {"name": "チェックリストの送付", "date": design_document_date - timedelta(days=5)}, 
            {"name": "試作日程の確保", "date": design_document_date - timedelta(days=5)},
            {"name": "要注意特許の確認", "date": design_document_date + timedelta(days=1)},
            {"name": "設計書後対応", "date": design_document_date},
            {"name": "美容剤、ソフト成分再確認", "date": design_document_date},
            {"name": "美容剤検討依頼書が届いているか確認", "date": design_document_date+ timedelta(days=10)},
            {"name": "安定性の設置", "date": design_document_date},
            {"name": "ベース、色決定", "date": specification_document_date - timedelta(days=7)},
            {"name": "読み合わせ", "date": specification_document_date - timedelta(days=7)},
            {"name": "チェックリストの送付", "date": specification_document_date - timedelta(days=7)},
            {"name": "マスタ統合入力", "date": specification_document_date - timedelta(days=7)},
            {"name": "美容剤決定報告書", "date": specification_document_date - timedelta(days=7)},
            {"name": "スケールアップの計量依頼枠確保", "date": specification_document_date - timedelta(days=7)},
            {"name": "特許確定", "date": specification_document_date + timedelta(days=14)},
            {"name": "製品情報プロファイルの処方の登録", "date": specification_document_date},
            {"name": "香料ランクC以上確認", "date": specification_document_date},
            {"name": "安定性、安全性、防腐確認", "date": specification_document_date},
            {"name": "美容剤確認表の返送", "date": specification_document_date + timedelta(days=7)},
            {"name": "試作充填依頼メールの送付", "date": trial_date - timedelta(days=42)},
            {"name": "試作願の提出", "date": trial_date - timedelta(days=30)},
            {"name": "スケールアップ", "date": trial_date - timedelta(days=35)},
            {"name": "製品技術概要", "date": trial_date - timedelta(days=14)},
            {"name": "試作見本品の送付", "date": trial_date - timedelta(days=7)},
            {"name": "事前打ち合わせ", "date": trial_date - timedelta(days=7)},
        ]
    # SPF測定なし、試作なし
    elif annual_classification == "no_spf" and prototype == "no_prototype":
        schedule = [
            {"name": "技打", "date": technical_meeting_date},
            {"name": "設計書", "date": design_document_date},
            {"name": "仕様書", "date": specification_document_date},
            {"name": "全成分", "date": all_ingredients_date}, 
            {"name": "ソフト成分、美容剤、訴求内容の確認", "date": technical_meeting_date}, 
            {"name": "製品符号を立ててもらう", "date": technical_meeting_date}, 
            {"name": "チェックリストの送付", "date": design_document_date - timedelta(days=5)}, 
            {"name": "要注意特許の確認", "date": design_document_date + timedelta(days=1)},
            {"name": "設計書後対応", "date": design_document_date},
            {"name": "美容剤、ソフト成分再確認", "date": design_document_date},
            {"name": "美容剤検討依頼書が届いているか確認", "date": design_document_date+ timedelta(days=10)},
            {"name": "安定性の設置", "date": design_document_date},
            {"name": "ベース、色決定", "date": specification_document_date - timedelta(days=7)},
            {"name": "読み合わせ", "date": specification_document_date - timedelta(days=7)},
            {"name": "チェックリストの送付", "date": specification_document_date - timedelta(days=7)},
            {"name": "マスタ統合入力", "date": specification_document_date - timedelta(days=7)},
            {"name": "美容剤決定報告書", "date": specification_document_date - timedelta(days=7)},
            {"name": "スケールアップの計量依頼枠確保", "date": specification_document_date - timedelta(days=7)},
            {"name": "特許確定", "date": specification_document_date + timedelta(days=14)},
            {"name": "製品情報プロファイルの処方の登録", "date": specification_document_date},
            {"name": "香料ランクC以上確認", "date": specification_document_date},
            {"name": "安定性、安全性、防腐確認", "date": specification_document_date},
            {"name": "美容剤確認表の返送", "date": specification_document_date + timedelta(days=7)},
        ]
    #SPF転用、試作あり    
    elif annual_classification == "spf_transfer" and prototype == "with_prototype":
        schedule = [
            {"name": "技打", "date": technical_meeting_date},
            {"name": "設計書", "date": design_document_date},
            {"name": "仕様書", "date": specification_document_date},
            {"name": "全成分", "date": all_ingredients_date},
            {"name": "機能性ユニットへの連絡", "date": technical_meeting_date}, 
            {"name": "ソフト成分、美容剤、訴求内容の確認", "date": technical_meeting_date}, 
            {"name": "製品符号を立ててもらう", "date": technical_meeting_date}, 
            {"name": "チェックリストの送付", "date": design_document_date - timedelta(days=5)}, 
            {"name": "試作日程の確保", "date": design_document_date - timedelta(days=5)},
            {"name": "要注意特許の確認", "date": design_document_date + timedelta(days=1)},
            {"name": "設計書後対応", "date": design_document_date},
            {"name": "美容剤、ソフト成分再確認", "date": design_document_date},
            {"name": "美容剤検討依頼書が届いているか確認", "date": design_document_date+ timedelta(days=10)},
            {"name": "安定性の設置", "date": design_document_date},
            {"name": "ベース、色決定", "date": specification_document_date - timedelta(days=7)},
            {"name": "読み合わせ", "date": specification_document_date - timedelta(days=7)},
            {"name": "チェックリストの送付", "date": specification_document_date - timedelta(days=7)},
            {"name": "マスタ統合入力", "date": specification_document_date - timedelta(days=7)},
            {"name": "美容剤決定報告書", "date": specification_document_date - timedelta(days=7)},
            {"name": "スケールアップの計量依頼枠確保", "date": specification_document_date - timedelta(days=7)},
            {"name": "特許確定", "date": specification_document_date + timedelta(days=14)},
            {"name": "製品情報プロファイルの処方の登録", "date": specification_document_date},
            {"name": "香料ランクC以上確認", "date": specification_document_date},
            {"name": "安定性、安全性、防腐確認", "date": specification_document_date},
            {"name": "美容剤確認表の返送", "date": specification_document_date + timedelta(days=7)},
            {"name": "試作充填依頼メールの送付", "date": trial_date - timedelta(days=42)},
            {"name": "試作願の提出", "date": trial_date - timedelta(days=30)},
            {"name": "スケールアップ", "date": trial_date - timedelta(days=35)},
            {"name": "製品技術概要", "date": trial_date - timedelta(days=14)},
            {"name": "試作見本品の送付", "date": trial_date - timedelta(days=7)},
            {"name": "事前打ち合わせ", "date": trial_date - timedelta(days=7)},
        ]
    #SPF転用、試作なし
    elif annual_classification == "spf_transfer" and prototype == "no_prototype":
        schedule = [
          {"name": "技打", "date": technical_meeting_date},
            {"name": "設計書", "date": design_document_date},
            {"name": "仕様書", "date": specification_document_date},
            {"name": "全成分", "date": all_ingredients_date},
            {"name": "機能性ユニットへの連絡", "date": technical_meeting_date}, 
            {"name": "ソフト成分、美容剤、訴求内容の確認", "date": technical_meeting_date}, 
            {"name": "製品符号を立ててもらう", "date": technical_meeting_date}, 
            {"name": "チェックリストの送付", "date": design_document_date - timedelta(days=5)}, 
            {"name": "要注意特許の確認", "date": design_document_date + timedelta(days=1)},
            {"name": "設計書後対応", "date": design_document_date},
            {"name": "美容剤、ソフト成分再確認", "date": design_document_date},
            {"name": "美容剤検討依頼書が届いているか確認", "date": design_document_date+ timedelta(days=10)},
            {"name": "安定性の設置", "date": design_document_date},
            {"name": "ベース、色決定", "date": specification_document_date - timedelta(days=7)},
            {"name": "読み合わせ", "date": specification_document_date - timedelta(days=7)},
            {"name": "チェックリストの送付", "date": specification_document_date - timedelta(days=7)},
            {"name": "マスタ統合入力", "date": specification_document_date - timedelta(days=7)},
            {"name": "美容剤決定報告書", "date": specification_document_date - timedelta(days=7)},
            {"name": "スケールアップの計量依頼枠確保", "date": specification_document_date - timedelta(days=7)},
            {"name": "特許確定", "date": specification_document_date + timedelta(days=14)},
            {"name": "製品情報プロファイルの処方の登録", "date": specification_document_date},
            {"name": "香料ランクC以上確認", "date": specification_document_date},
            {"name": "安定性、安全性、防腐確認", "date": specification_document_date},
            {"name": "美容剤確認表の返送", "date": specification_document_date + timedelta(days=7)},
        ]
    #アレテノンコメあり、試作あり
    elif annual_classification == "aretenon" and prototype == "with_prototype":
        schedule = [
            {"name": "技打", "date": technical_meeting_date},
            {"name": "設計書", "date": design_document_date},
            {"name": "仕様書", "date": specification_document_date},
            {"name": "全成分", "date": all_ingredients_date},
            {"name": "安全性への連絡", "date": technical_meeting_date}, 
            {"name": "ソフト成分、美容剤、訴求内容の確認", "date": technical_meeting_date}, 
            {"name": "製品符号を立ててもらう", "date": technical_meeting_date}, 
            {"name": "チェックリストの送付", "date": design_document_date - timedelta(days=5)}, 
            {"name": "試作日程の確保", "date": design_document_date - timedelta(days=5)},
            {"name": "要注意特許の確認", "date": design_document_date + timedelta(days=1)},
            {"name": "設計書後対応", "date": design_document_date},
            {"name": "美容剤、ソフト成分再確認", "date": design_document_date},
            {"name": "美容剤検討依頼書が届いているか確認", "date": design_document_date+ timedelta(days=10)},
            {"name": "安定性の設置", "date": design_document_date},
            {"name": "ベース、色決定", "date": specification_document_date - timedelta(days=7)},
            {"name": "読み合わせ", "date": specification_document_date - timedelta(days=7)},
            {"name": "チェックリストの送付", "date": specification_document_date - timedelta(days=7)},
            {"name": "マスタ統合入力", "date": specification_document_date - timedelta(days=7)},
            {"name": "美容剤決定報告書", "date": specification_document_date - timedelta(days=7)},
            {"name": "スケールアップの計量依頼枠確保", "date": specification_document_date - timedelta(days=7)},
            {"name": "特許確定", "date": specification_document_date + timedelta(days=14)},
            {"name": "製品情報プロファイルの処方の登録", "date": specification_document_date},
            {"name": "香料ランクC以上確認", "date": specification_document_date},
            {"name": "安定性、安全性、防腐確認", "date": specification_document_date},
            {"name": "美容剤確認表の返送", "date": specification_document_date + timedelta(days=7)},
            {"name": "試作充填依頼メールの送付", "date": trial_date - timedelta(days=42)},
            {"name": "試作願の提出", "date": trial_date - timedelta(days=30)},
            {"name": "スケールアップ", "date": trial_date - timedelta(days=35)},
            {"name": "製品技術概要", "date": trial_date - timedelta(days=14)},
            {"name": "試作見本品の送付", "date": trial_date - timedelta(days=7)},
            {"name": "事前打ち合わせ", "date": trial_date - timedelta(days=7)},
        ]
        if response_date:
            schedule.append({"name": "アレテノンコメバルク提出", "date": response_date - timedelta(days=120)})
            
    #アレテノンコメあり、試作なし
    elif annual_classification == "aretenon" and prototype == "no_prototype":
        schedule = [
             {"name": "技打", "date": technical_meeting_date},
            {"name": "設計書", "date": design_document_date},
            {"name": "仕様書", "date": specification_document_date},
            {"name": "全成分", "date": all_ingredients_date},
            {"name": "安全性への連絡", "date": technical_meeting_date}, 
            {"name": "ソフト成分、美容剤、訴求内容の確認", "date": technical_meeting_date}, 
            {"name": "製品符号を立ててもらう", "date": technical_meeting_date}, 
            {"name": "チェックリストの送付", "date": design_document_date - timedelta(days=5)}, 
            {"name": "要注意特許の確認", "date": design_document_date + timedelta(days=1)},
            {"name": "設計書後対応", "date": design_document_date},
            {"name": "美容剤、ソフト成分再確認", "date": design_document_date},
            {"name": "美容剤検討依頼書が届いているか確認", "date": design_document_date+ timedelta(days=10)},
            {"name": "安定性の設置", "date": design_document_date},
            {"name": "ベース、色決定", "date": specification_document_date - timedelta(days=7)},
            {"name": "読み合わせ", "date": specification_document_date - timedelta(days=7)},
            {"name": "チェックリストの送付", "date": specification_document_date - timedelta(days=7)},
            {"name": "マスタ統合入力", "date": specification_document_date - timedelta(days=7)},
            {"name": "美容剤決定報告書", "date": specification_document_date - timedelta(days=7)},
            {"name": "スケールアップの計量依頼枠確保", "date": specification_document_date - timedelta(days=7)},
            {"name": "特許確定", "date": specification_document_date + timedelta(days=14)},
            {"name": "製品情報プロファイルの処方の登録", "date": specification_document_date},
            {"name": "香料ランクC以上確認", "date": specification_document_date},
            {"name": "安定性、安全性、防腐確認", "date": specification_document_date},
            {"name": "美容剤確認表の返送", "date": specification_document_date + timedelta(days=7)},
        ]
        if response_date:
            schedule.append({"name": "アレテノンコメバルク提出", "date": response_date - timedelta(days=120)})
            
    # アレテノンコメなし、試作あり
    elif annual_classification == "no_aretenon" and prototype == "with_prototype":
        schedule = [
            {"name": "技打", "date": technical_meeting_date},
            {"name": "設計書", "date": design_document_date},
            {"name": "仕様書", "date": specification_document_date},
            {"name": "全成分", "date": all_ingredients_date},
            {"name": "ソフト成分、美容剤、訴求内容の確認", "date": technical_meeting_date}, 
            {"name": "製品符号を立ててもらう", "date": technical_meeting_date}, 
            {"name": "チェックリストの送付", "date": design_document_date - timedelta(days=5)}, 
            {"name": "試作日程の確保", "date": design_document_date - timedelta(days=5)},
            {"name": "要注意特許の確認", "date": design_document_date + timedelta(days=1)},
            {"name": "設計書後対応", "date": design_document_date},
            {"name": "美容剤、ソフト成分再確認", "date": design_document_date},
            {"name": "美容剤検討依頼書が届いているか確認", "date": design_document_date+ timedelta(days=10)},
            {"name": "安定性の設置", "date": design_document_date},
            {"name": "ベース、色決定", "date": specification_document_date - timedelta(days=7)},
            {"name": "読み合わせ", "date": specification_document_date - timedelta(days=7)},
            {"name": "チェックリストの送付", "date": specification_document_date - timedelta(days=7)},
            {"name": "マスタ統合入力", "date": specification_document_date - timedelta(days=7)},
            {"name": "美容剤決定報告書", "date": specification_document_date - timedelta(days=7)},
            {"name": "スケールアップの計量依頼枠確保", "date": specification_document_date - timedelta(days=7)},
            {"name": "特許確定", "date": specification_document_date + timedelta(days=14)},
            {"name": "製品情報プロファイルの処方の登録", "date": specification_document_date},
            {"name": "香料ランクC以上確認", "date": specification_document_date},
            {"name": "安定性、安全性、防腐確認", "date": specification_document_date},
            {"name": "美容剤確認表の返送", "date": specification_document_date + timedelta(days=7)},
            {"name": "試作充填依頼メールの送付", "date": trial_date - timedelta(days=42)},
            {"name": "試作願の提出", "date": trial_date - timedelta(days=30)},
            {"name": "スケールアップ", "date": trial_date - timedelta(days=35)},
            {"name": "製品技術概要", "date": trial_date - timedelta(days=14)},
            {"name": "試作見本品の送付", "date": trial_date - timedelta(days=7)},
            {"name": "事前打ち合わせ", "date": trial_date - timedelta(days=7)},
        ]
    # アレテノンコメなし、試作なし
    elif annual_classification == "no_aretenon" and prototype == "no_prototype":
        schedule = [
            {"name": "技打", "date": technical_meeting_date},
            {"name": "設計書", "date": design_document_date},
            {"name": "仕様書", "date": specification_document_date},
            {"name": "全成分", "date": all_ingredients_date}, 
            {"name": "ソフト成分、美容剤、訴求内容の確認", "date": technical_meeting_date}, 
            {"name": "製品符号を立ててもらう", "date": technical_meeting_date}, 
            {"name": "チェックリストの送付", "date": design_document_date - timedelta(days=5)}, 
            {"name": "要注意特許の確認", "date": design_document_date + timedelta(days=1)},
            {"name": "設計書後対応", "date": design_document_date},
            {"name": "美容剤、ソフト成分再確認", "date": design_document_date},
            {"name": "美容剤検討依頼書が届いているか確認", "date": design_document_date+ timedelta(days=10)},
            {"name": "安定性の設置", "date": design_document_date},
            {"name": "ベース、色決定", "date": specification_document_date - timedelta(days=7)},
            {"name": "読み合わせ", "date": specification_document_date - timedelta(days=7)},
            {"name": "チェックリストの送付", "date": specification_document_date - timedelta(days=7)},
            {"name": "マスタ統合入力", "date": specification_document_date - timedelta(days=7)},
            {"name": "美容剤決定報告書", "date": specification_document_date - timedelta(days=7)},
            {"name": "スケールアップの計量依頼枠確保", "date": specification_document_date - timedelta(days=7)},
            {"name": "特許確定", "date": specification_document_date + timedelta(days=14)},
            {"name": "製品情報プロファイルの処方の登録", "date": specification_document_date},
            {"name": "香料ランクC以上確認", "date": specification_document_date},
            {"name": "安定性、安全性、防腐確認", "date": specification_document_date},
            {"name": "美容剤確認表の返送", "date": specification_document_date + timedelta(days=7)},
        ]
    
    #SPF,アレテノンコメあり、試作あり
    elif annual_classification == "spf_and_aretenon" and prototype == "with_prototype":
        schedule = [
            {"name": "技打", "date": technical_meeting_date},
            {"name": "設計書", "date": design_document_date},
            {"name": "仕様書", "date": specification_document_date},
            {"name": "全成分", "date": all_ingredients_date},
            {"name": "機能性,安全性ユニットへの連絡", "date": technical_meeting_date}, 
            {"name": "ソフト成分、美容剤、訴求内容の確認", "date": technical_meeting_date}, 
            {"name": "製品符号を立ててもらう", "date": technical_meeting_date}, 
            {"name": "チェックリストの送付", "date": design_document_date - timedelta(days=5)}, 
            {"name": "試作日程の確保", "date": design_document_date - timedelta(days=5)},
            {"name": "要注意特許の確認", "date": design_document_date + timedelta(days=1)},
            {"name": "設計書後対応", "date": design_document_date},
            {"name": "美容剤、ソフト成分再確認", "date": design_document_date},
            {"name": "美容剤検討依頼書が届いているか確認", "date": design_document_date+ timedelta(days=10)},
            {"name": "安定性の設置", "date": design_document_date},
            {"name": "ベース、色決定", "date": specification_document_date - timedelta(days=7)},
            {"name": "読み合わせ", "date": specification_document_date - timedelta(days=7)},
            {"name": "チェックリストの送付", "date": specification_document_date - timedelta(days=7)},
            {"name": "マスタ統合入力", "date": specification_document_date - timedelta(days=7)},
            {"name": "美容剤決定報告書", "date": specification_document_date - timedelta(days=7)},
            {"name": "スケールアップの計量依頼枠確保", "date": specification_document_date - timedelta(days=7)},
            {"name": "特許確定", "date": specification_document_date + timedelta(days=14)},
            {"name": "製品情報プロファイルの処方の登録", "date": specification_document_date},
            {"name": "香料ランクC以上確認", "date": specification_document_date},
            {"name": "安定性、安全性、防腐確認", "date": specification_document_date},
            {"name": "美容剤確認表の返送", "date": specification_document_date + timedelta(days=7)},
            {"name": "試作充填依頼メールの送付", "date": trial_date - timedelta(days=42)},
            {"name": "試作願の提出", "date": trial_date - timedelta(days=30)},
            {"name": "スケールアップ", "date": trial_date - timedelta(days=35)},
            {"name": "製品技術概要", "date": trial_date - timedelta(days=14)},
            {"name": "試作見本品の送付", "date": trial_date - timedelta(days=7)},
            {"name": "事前打ち合わせ", "date": trial_date - timedelta(days=7)},
        ]
        if response_date:
            schedule.append({"name": "SPFバルク提出", "date": response_date - timedelta(days=150)})
            schedule.append({"name": "アレテノンコメバルク提出", "date": response_date - timedelta(days=120)})
    
    
    # SPF,アレテノンコメあり、試作なし
    elif annual_classification == "spf_and_aretenon" and prototype == "no_prototype":
        schedule = [
            {"name": "技打", "date": technical_meeting_date},
            {"name": "設計書", "date": design_document_date},
            {"name": "仕様書", "date": specification_document_date},
            {"name": "全成分", "date": all_ingredients_date},
            {"name": "機能性,安全性ユニットへの連絡", "date": technical_meeting_date}, 
            {"name": "ソフト成分、美容剤、訴求内容の確認", "date": technical_meeting_date}, 
            {"name": "製品符号を立ててもらう", "date": technical_meeting_date}, 
            {"name": "チェックリストの送付", "date": design_document_date - timedelta(days=5)}, 
            {"name": "要注意特許の確認", "date": design_document_date + timedelta(days=1)},
            {"name": "設計書後対応", "date": design_document_date},
            {"name": "美容剤、ソフト成分再確認", "date": design_document_date},
            {"name": "美容剤検討依頼書が届いているか確認", "date": design_document_date+ timedelta(days=10)},
            {"name": "安定性の設置", "date": design_document_date},
            {"name": "ベース、色決定", "date": specification_document_date - timedelta(days=7)},
            {"name": "読み合わせ", "date": specification_document_date - timedelta(days=7)},
            {"name": "チェックリストの送付", "date": specification_document_date - timedelta(days=7)},
            {"name": "マスタ統合入力", "date": specification_document_date - timedelta(days=7)},
            {"name": "美容剤決定報告書", "date": specification_document_date - timedelta(days=7)},
            {"name": "スケールアップの計量依頼枠確保", "date": specification_document_date - timedelta(days=7)},
            {"name": "特許確定", "date": specification_document_date + timedelta(days=14)},
            {"name": "製品情報プロファイルの処方の登録", "date": specification_document_date},
            {"name": "香料ランクC以上確認", "date": specification_document_date},
            {"name": "安定性、安全性、防腐確認", "date": specification_document_date},
            {"name": "美容剤確認表の返送", "date": specification_document_date + timedelta(days=7)},
        ]
        if response_date:
            schedule.append({"name": "SPFバルク提出", "date": response_date - timedelta(days=150)})
            schedule.append({"name": "アレテノンコメバルク提出", "date": response_date - timedelta(days=120)})
            
    # SPF,アレテノンコメなし、試作あり
    elif annual_classification == "no_spf_and_aretenon" and prototype == "with_prototype":
        schedule = [
            {"name": "技打", "date": technical_meeting_date},
            {"name": "設計書", "date": design_document_date},
            {"name": "仕様書", "date": specification_document_date},
            {"name": "全成分", "date": all_ingredients_date},
            {"name": "ソフト成分、美容剤、訴求内容の確認", "date": technical_meeting_date}, 
            {"name": "製品符号を立ててもらう", "date": technical_meeting_date}, 
            {"name": "チェックリストの送付", "date": design_document_date - timedelta(days=5)}, 
            {"name": "試作日程の確保", "date": design_document_date - timedelta(days=5)},
            {"name": "要注意特許の確認", "date": design_document_date + timedelta(days=1)},
            {"name": "設計書後対応", "date": design_document_date},
            {"name": "美容剤、ソフト成分再確認", "date": design_document_date},
            {"name": "美容剤検討依頼書が届いているか確認", "date": design_document_date+ timedelta(days=10)},
            {"name": "安定性の設置", "date": design_document_date},
            {"name": "ベース、色決定", "date": specification_document_date - timedelta(days=7)},
            {"name": "読み合わせ", "date": specification_document_date - timedelta(days=7)},
            {"name": "チェックリストの送付", "date": specification_document_date - timedelta(days=7)},
            {"name": "マスタ統合入力", "date": specification_document_date - timedelta(days=7)},
            {"name": "美容剤決定報告書", "date": specification_document_date - timedelta(days=7)},
            {"name": "スケールアップの計量依頼枠確保", "date": specification_document_date - timedelta(days=7)},
            {"name": "特許確定", "date": specification_document_date + timedelta(days=14)},
            {"name": "製品情報プロファイルの処方の登録", "date": specification_document_date},
            {"name": "香料ランクC以上確認", "date": specification_document_date},
            {"name": "安定性、安全性、防腐確認", "date": specification_document_date},
            {"name": "美容剤確認表の返送", "date": specification_document_date + timedelta(days=7)},
            {"name": "試作充填依頼メールの送付", "date": trial_date - timedelta(days=42)},
            {"name": "試作願の提出", "date": trial_date - timedelta(days=30)},
            {"name": "スケールアップ", "date": trial_date - timedelta(days=35)},
            {"name": "製品技術概要", "date": trial_date - timedelta(days=14)},
            {"name": "試作見本品の送付", "date": trial_date - timedelta(days=7)},
            {"name": "事前打ち合わせ", "date": trial_date - timedelta(days=7)},
        ]
    # SPF,アレテノンコメなし、試作なし
    elif annual_classification == "no_spf_and_aretenon" and prototype == "no_prototype":
        schedule = [
            {"name": "技打", "date": technical_meeting_date},
            {"name": "設計書", "date": design_document_date},
            {"name": "仕様書", "date": specification_document_date},
            {"name": "全成分", "date": all_ingredients_date}, 
            {"name": "ソフト成分、美容剤、訴求内容の確認", "date": technical_meeting_date}, 
            {"name": "製品符号を立ててもらう", "date": technical_meeting_date}, 
            {"name": "チェックリストの送付", "date": design_document_date - timedelta(days=5)}, 
            {"name": "要注意特許の確認", "date": design_document_date + timedelta(days=1)},
            {"name": "設計書後対応", "date": design_document_date},
            {"name": "美容剤、ソフト成分再確認", "date": design_document_date},
            {"name": "美容剤検討依頼書が届いているか確認", "date": design_document_date+ timedelta(days=10)},
            {"name": "安定性の設置", "date": design_document_date},
            {"name": "ベース、色決定", "date": specification_document_date - timedelta(days=7)},
            {"name": "読み合わせ", "date": specification_document_date - timedelta(days=7)},
            {"name": "チェックリストの送付", "date": specification_document_date - timedelta(days=7)},
            {"name": "マスタ統合入力", "date": specification_document_date - timedelta(days=7)},
            {"name": "美容剤決定報告書", "date": specification_document_date - timedelta(days=7)},
            {"name": "スケールアップの計量依頼枠確保", "date": specification_document_date - timedelta(days=7)},
            {"name": "特許確定", "date": specification_document_date + timedelta(days=14)},
            {"name": "製品情報プロファイルの処方の登録", "date": specification_document_date},
            {"name": "香料ランクC以上確認", "date": specification_document_date},
            {"name": "安定性、安全性、防腐確認", "date": specification_document_date},
            {"name": "美容剤確認表の返送", "date": specification_document_date + timedelta(days=7)},
        ]


        
    # 結果ページにデータを渡す
    return render_template(
    "result.html",
    schedule=schedule,
    technical_meeting=technical_meeting_date,
    design_document=design_document_date,
    specification_document=specification_document_date,
    all_ingredients=all_ingredients_date,
    trial_date=trial_date,
    prototype=prototype,
    response_date=response_date,
    result=result  
)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)