from flask import Flask, render_template, request, redirect, url_for, send_file
import datetime
import lunardate
from wtforms import StringField, IntegerField, validators
from flask_wtf import FlaskForm
# Danh sách các Thiên Can và Địa Chi
heavenly_stems = ["Giáp", "Ất", "Bính", "Đinh",
                  "Mậu", "Kỷ", "Canh", "Tân", "Nhâm", "Quý"]
earthly_branches = ["Tý", "Sửu", "Dần", "Mão", "Thìn",
                    "Tỵ", "Ngọ", "Mùi", "Thân", "Dậu", "Tuất", "Hợi"]

# Ngũ hành của Thiên Can và Địa Chi
heavenly_stem_elements = {
    "Giáp": "Mộc", "Ất": "Mộc", "Bính": "Hỏa", "Đinh": "Hỏa",
    "Mậu": "Thổ", "Kỷ": "Thổ", "Canh": "Kim", "Tân": "Kim",
    "Nhâm": "Thủy", "Quý": "Thủy"
}

earthly_branch_elements = {
    "Tý": "Thủy", "Sửu": "Thổ", "Dần": "Mộc", "Mão": "Mộc",
    "Thìn": "Thổ", "Tỵ": "Hỏa", "Ngọ": "Hỏa", "Mùi": "Thổ",
    "Thân": "Kim", "Dậu": "Kim", "Tuất": "Thổ", "Hợi": "Thủy"
}

dict_hexagram = {
    '__________________': {'name': 'Bát Thuần Kiền', 'icon': 'images/1.jpg'},
    '_ __ __ __ __ __ _': {'name': 'Bát Thuần Khôn', 'icon': 'images/2.jpg'},
    '_ _____ __ __ ____': {'name': 'Thủy Lôi Truân', 'icon': 'images/3.jpg'},
    '____ __ __ _____ _': {'name': 'Sơn Thủy Mông', 'icon': 'images/4.jpg'},
    '_ _____ __________': {'name': 'Thủy Thiên Nhu', 'icon': 'images/5.jpg'},
    '__________ _____ _': {'name': 'Thiên Thủy Tụng', 'icon': 'images/6.gif'},
    '_ __ __ __ _____ _': {'name': 'Địa Thủy Sư', 'icon': 'images/7.gif'},
    '_ _____ __ __ __ _': {'name': 'Thủy Địa Tỷ', 'icon': 'images/8.gif'},
    '_______ __________': {'name': 'Phong Thiên Tiểu Súc', 'icon': 'images/9.gif'},
    '__________ _______': {'name': 'Thiên Trạch Lý', 'icon': 'images/10.gif'},
    '_ __ __ __________': {'name': 'Địa Thiên Thái', 'icon': 'images/11.gif'},
    '__________ __ __ _': {'name': 'Thiên Địa Bĩ', 'icon': 'images/12.gif'},
    '_____________ ____': {'name': 'Thiên Hỏa Đồng Nhân', 'icon': 'images/13.gif'},
    '____ _____________': {'name': 'Hỏa Thiên Đại Hữu', 'icon': 'images/14.gif'},
    '_ __ __ _____ __ _': {'name': 'Địa Sơn Khiêm', 'icon': 'images/15.gif'},
    '_ __ _____ __ __ _': {'name': 'Lôi Địa Dự', 'icon': 'images/16.gif'},
    '_ ________ __ ____': {'name': 'Trạch Lôi Tùy', 'icon': 'images/17.gif'},
    '____ __ ________ _': {'name': 'Sơn Phong Cổ', 'icon': 'images/18.gif'},
    '_ __ __ __ _______': {'name': 'Địa Trạch Lâm', 'icon': 'images/19.gif'},
    '_______ __ __ __ _': {'name': 'Phong Địa Quán', 'icon': 'images/20.gif'},
    '____ _____ __ ____': {'name': 'Hỏa Lôi Phệ Hạp', 'icon': 'images/21.gif'},
    '____ __ _____ ____': {'name': 'Sơn Hỏa Bí', 'icon': 'images/22.gif'},
    '____ __ __ __ __ _': {'name': 'Sơn Địa Bác', 'icon': 'images/23.gif'},
    '_ __ __ __ __ ____': {'name': 'Địa Lôi Phục', 'icon': 'images/24.gif'},
    '__________ __ ____': {'name': 'Thiên Lôi Vô Vọng', 'icon': 'images/25.gif'},
    '____ __ __________': {'name': 'Sơn Thiên Đại Súc', 'icon': 'images/26.gif'},
    '____ __ __ __ ____': {'name': 'Sơn Lôi Di', 'icon': 'images/27.gif'},
    '_ ______________ _': {'name': 'Trạch Phong Đại Quá', 'icon': 'images/28.gif'},
    '_ _____ __ _____ _': {'name': 'Khảm Vi Thủy', 'icon': 'images/29.gif'},
    '____ ________ ____': {'name': 'Ly Vi Hỏa', 'icon': 'images/30.gif'},
    '_ ___________ __ _': {'name': 'Trạch Sơn Hàm', 'icon': 'images/31.gif'},
    '_ __ ___________ _': {'name': 'Lôi Phong Hằng', 'icon': 'images/32.gif'},
    '_____________ __ _': {'name': 'Thiên Sơn Độn', 'icon': 'images/33.gif'},
    '_ __ _____________': {'name': 'Lôi Thiên Đại Tráng', 'icon': 'images/34.gif'},
    '____ _____ __ __ _': {'name': 'Hỏa Địa Tấn', 'icon': 'images/35.gif'},
    '_ __ __ _____ ____': {'name': 'Địa Hỏa Minh Di', 'icon': 'images/36.gif'},
    '_______ _____ ____': {'name': 'Phong Hỏa Gia Nhân', 'icon': 'images/37.gif'},
    '____ _____ _______': {'name': 'Hỏa Trạch Khuê', 'icon': 'images/38.gif'},
    '_ _____ _____ __ _': {'name': 'Thủy Sơn Kiển', 'icon': 'images/39.gif'},
    '_ __ _____ _____ _': {'name': 'Lôi Thủy Giải', 'icon': 'images/40.gif'},
    '____ __ __ _______': {'name': 'Sơn Trạch Tổn', 'icon': 'images/41.gif'},
    '_______ __ __ ____': {'name': 'Phong Lôi Ích', 'icon': 'images/42.gif'},
    '_ ________________': {'name': 'Trạch Thiên Quải', 'icon': 'images/43.gif'},
    '________________ _': {'name': 'Thiên Phong Cấu', 'icon': 'images/44.gif'},
    '_ ________ __ __ _': {'name': 'Trạch Địa Tụy', 'icon': 'images/45.gif'},
    '_ __ __ ________ _': {'name': 'Địa Phong Thăng', 'icon': 'images/46.gif'},
    '_ ________ _____ _': {'name': 'Trạch Thủy Khốn', 'icon': 'images/47.gif'},
    '_ _____ ________ _': {'name': 'Thủy Phong Tỉnh', 'icon': 'images/48.gif'},
    '_ ___________ ____': {'name': 'Trạch Hỏa Cách', 'icon': 'images/49.gif'},
    '____ ___________ _': {'name': 'Hỏa Phong Đỉnh', 'icon': 'images/50.gif'},
    '_ __ _____ __ ____': {'name': 'Chấn Vi Lôi', 'icon': 'images/51.gif'},
    '____ __ _____ __ _': {'name': 'Cấn Vi Sơn', 'icon': 'images/52.gif'},
    '_______ _____ __ _': {'name': 'Phong Sơn Tiệm', 'icon': 'images/53.gif'},
    '_ __ _____ _______': {'name': 'Lôi Trạch Quy Muội', 'icon': 'images/54.gif'},
    '_ __ ________ ____': {'name': 'Lôi Hỏa Phong', 'icon': 'images/55.gif'},
    '____ ________ __ _': {'name': 'Hỏa Sơn Lữ', 'icon': 'images/56.gif'},
    '_______ ________ _': {'name': 'Tốn Vi Phong', 'icon': 'images/57.gif'},
    '_ ________ _______': {'name': 'Đoài Vi Trạch', 'icon': 'images/58.gif'},
    '_______ __ _____ _': {'name': 'Phong Thủy Hoán', 'icon': 'images/59.gif'},
    '_ _____ __ _______': {'name': 'Thủy Trạch Tiết', 'icon': 'images/60.gif'},
    '_______ __ _______': {'name': 'Phong Trạch Trung Phu', 'icon': 'images/61.gif'},
    '_ __ ________ __ _': {'name': 'Lôi Sơn Tiểu Quá', 'icon': 'images/62.gif'},
    '_ _____ _____ ____': {'name': 'Thủy Hỏa Ký Tế', 'icon': 'images/63.gif'},
    '____ _____ _____ _': {'name': 'Hỏa Thủy Vị Tế', 'icon': 'images/64.gif'},

}
app = Flask(__name__)
# Necessary for Flask-WTF forms
app.config['SECRET_KEY'] = 'your_secret_key_here'


# WTForms Form
class InputForm(FlaskForm):
    name = StringField('Họ và tên', [validators.InputRequired()])
    year = IntegerField('Năm sinh', [validators.InputRequired(
    ), validators.NumberRange(min=1900, max=datetime.datetime.now().year)])
    month = IntegerField('Tháng sinh', [
                         validators.InputRequired(), validators.NumberRange(min=1, max=12)])
    day = IntegerField('Ngày sinh', [
                       validators.InputRequired(), validators.NumberRange(min=1, max=31)])
    hour = IntegerField(
        'Giờ sinh (0-23)', [validators.InputRequired(), validators.NumberRange(min=0, max=23)])


def convert_gregorian_to_lunar(year, month, day):
    """
    Chuyển đổi dương lịch sang âm lịch
    """
    gregorian_date = datetime.date(year, month, day)
    lunar_date = lunardate.LunarDate.fromSolarDate(
        gregorian_date.year, gregorian_date.month, gregorian_date.day)
    return lunar_date


def calculate_stem_and_branch(lunar_year, lunar_month, lunar_day, hour):
    """
    Hàm tính thiên can và địa chi
    """
    heavenly_stem_year = heavenly_stems[(lunar_year - 3) % 10]
    earthly_branch_year = earthly_branches[(lunar_year - 3) % 12]

    heavenly_stem_month = heavenly_stems[(lunar_year * 12 + lunar_month) % 10]
    earthly_branch_month = earthly_branches[(lunar_month + 1) % 12]

    heavenly_stem_day = heavenly_stems[(lunar_day + 10) % 10]
    earthly_branch_day = earthly_branches[(lunar_day + 12) % 12]

    hour_to_branch = {23: "Tý", 1: "Sửu", 3: "Dần", 5: "Mão", 7: "Thìn", 9: "Tỵ",
                      11: "Ngọ", 13: "Mùi", 15: "Thân", 17: "Dậu", 19: "Tuất", 21: "Hợi"}
    earthly_branch_hour = hour_to_branch[hour]

    return {
        'year': (heavenly_stem_year, earthly_branch_year),
        'month': (heavenly_stem_month, earthly_branch_month),
        'day': (heavenly_stem_day, earthly_branch_day),
        'hour': ('', earthly_branch_hour)  # Chỉ cần Địa Chi cho giờ
    }


def calculate_hexagram_by_branch_birth(branch_birth):
    # Dùng bảng tra để chuyển đổi Địa Chi thành hào
    branch_to_lines = {
        "Tý": "___",  # Ví dụ: gạch liền
        "Sửu": "_ _",  # Ví dụ: gạch đứt
        "Dần": "___",
        "Mão": "_ _",
        "Thìn": "___",
        "Tỵ": "_ _",
        "Ngọ": "___",
        "Mùi": "_ _",
        "Thân": "___",
        "Dậu": "_ _",
        "Tuất": "___",
        "Hợi": "_ _"
    }

    # Nội quẻ: 3 hào từ Địa Chi của năm sinh
    inner_hexagram = [
        branch_to_lines[branch_birth],   # Hào 1
        # Hào 2 (Giả định lặp lại để đơn giản hóa)
        branch_to_lines[branch_birth],
        branch_to_lines[branch_birth]     # Hào 3
    ]

    # Ngoại quẻ: 3 hào từ Địa Chi của năm sinh
    outer_hexagram = [
        branch_to_lines[branch_birth],    # Hào 4
        branch_to_lines[branch_birth],   # Hào 5
        branch_to_lines[branch_birth]    # Hào 6
    ]

    return inner_hexagram, outer_hexagram


def calculate_hexagram(chart):
    # Dùng bảng tra để chuyển đổi Địa Chi thành hào
    branch_to_lines = {
        "Tý": "___",  # Ví dụ: gạch liền
        "Sửu": "_ _",  # Ví dụ: gạch đứt
        "Dần": "___",
        "Mão": "_ _",
        "Thìn": "___",
        "Tỵ": "_ _",
        "Ngọ": "___",
        "Mùi": "_ _",
        "Thân": "___",
        "Dậu": "_ _",
        "Tuất": "___",
        "Hợi": "_ _"
    }

    # Nội quẻ: 3 hào từ Địa Chi của năm, tháng và ngày
    inner_hexagram = [
        branch_to_lines[chart['year'][1]],   # Hào 1
        branch_to_lines[chart['month'][1]],  # Hào 2
        branch_to_lines[chart['day'][1]]     # Hào 3
    ]

    # Ngoại quẻ: 3 hào từ Địa Chi của ngày, giờ và năm
    outer_hexagram = [
        branch_to_lines[chart['day'][1]],    # Hào 4
        branch_to_lines[chart['hour'][1]],   # Hào 5
        branch_to_lines[chart['year'][1]]    # Hào 6
    ]

    return inner_hexagram, outer_hexagram

# Hàm luận giải thêm cho Nội quẻ và Ngoại quẻ


def interpret_hexagram(inner, outer):
    interpretation = f"Nội quẻ: {' '.join(inner)}\nNgoại quẻ: {
        ' '.join(outer)}\n\n"
    interpretation += "Luận giải sơ bộ:\n"
    if inner == ["___", "___", "___"]:
        interpretation += "Nội quẻ biểu hiện sự cương nghị và mạnh mẽ trong Tiền Vận.\n"
    if outer == ["_ _", "_ _", "_ _"]:
        interpretation += "Ngoại quẻ thể hiện cần sự mềm mỏng và thích nghi trong Hậu Vận.\n"
    # Cập nhật thêm luận giải chi tiết cho từng trường hợp
    return interpretation

# Luận giải chi tiết theo khía cạnh


# def interpret_life_aspects(chart):
#     aspects = []
#     aspects.append(
#         "1. Công danh: Trong Tiền Vận, nỗ lực cá nhân có thể đưa đến thành công lớn nếu biết điều chỉnh hài hòa với hoàn cảnh.\n")
#     aspects.append(
#         "2. Tình duyên: Quẻ thể hiện sự bền vững trong tình cảm nếu biết kiên nhẫn.\n")
#     aspects.append(
#         "3. Tiền bạc: Tiền bạc sẽ thăng trầm theo chu kỳ của cuộc sống, cần quản lý chặt chẽ.\n")
#     aspects.append(
#         "4. Sức khỏe: Sức khỏe tốt trong Tiền Vận nhưng cần chú ý bảo dưỡng trong Hậu Vận.\n")
#     return "\n".join(aspects)


# Hàm luận giải
# def interpret_ba_tu_chart(chart):
#     interpretations = []
#     interpretations.append(f"Năm sinh Thiên Can là {
#                            chart['year'][0]}, Địa Chi là {chart['year'][1]}.")
#     interpretations.append(f"Tháng sinh Thiên Can là {
#                            chart['month'][0]}, Địa Chi là {chart['month'][1]}.")
#     interpretations.append(f"Ngày sinh Thiên Can là {
#                            chart['day'][0]}, Địa Chi là {chart['day'][1]}.")
#     interpretations.append(f"Giờ sinh Thiên Can là {
#                            chart['hour'][0]}, Địa Chi là {chart['hour'][1]}.")

#     # Tính Nội quẻ và Ngoại quẻ
#     inner_hexagram, outer_hexagram = calculate_hexagram(chart)

#     # Thêm phần luận giải Nội quẻ và Ngoại quẻ
#     luan_giai = interpret_hexagram(inner_hexagram, outer_hexagram)

#     # Thêm phần luận giải khía cạnh cuộc sống
#     luan_giai_cuoc_song = interpret_life_aspects(chart)

#     # return "\n".join(interpretations)
#     return inner_hexagram, outer_hexagram, luan_giai, luan_giai_cuoc_song

def calc_heavenly_earthly_by_chart(chart):
    """
    tính thiên can dựa vào ngày
    """
    heavenly_by_birth = [chart['year'][0], chart['month']
                         [0], chart['day'][0], chart['hour'][0]]
    earthly_by_birth = [chart['year'][1], chart['month']
                        [1], chart['day'][1], chart['hour'][1]]
    return heavenly_by_birth, earthly_by_birth


# Route for form input and result display
@app.route('/', methods=['GET', 'POST'])
def index():
    form = InputForm(request.form)
    if request.method == 'POST' and form.validate():
        # Lấy thông tin từ form
        name = form.name.data
        year_of_birth = form.year.data
        month_of_birth = form.month.data
        day_of_birth = form.day.data
        hour_of_birth = form.hour.data

        # Chuyển dương lịch sang âm lịch
        lunar_date = convert_gregorian_to_lunar(
            year_of_birth, month_of_birth, day_of_birth)

        # Calculate Bát Tự chart
        chart = calculate_stem_and_branch(
            lunar_date.year, lunar_date.month, lunar_date.day, hour_of_birth)

        # Tính thiên can và địa chi dựa vào chart
        heavenly_by_birth, earthly_by_birth = calc_heavenly_earthly_by_chart(
            chart)

        # Tính nội quẻ và ngoại quẻ
        inner_hexagram_of_birth, outer_hexagram_of_birth = calculate_hexagram(
            chart)

        shape = ''.join(inner_hexagram_of_birth + outer_hexagram_of_birth)
        hexagram_of_birth = dict_hexagram.get(shape)

        # region Tính theo năm
        year_range = range(1990, 2050)

        # Thiên can và địa chi theo năm sinh
        year_heavenly_by_birth = heavenly_by_birth[0]
        year_earthly_by_birth = earthly_by_birth[0]

        results = {}
        # Luận giải vận hạn từ 1990 tới 2050 với hào động
        for seen_year in range(1990, 2051):
            # thiên can, địa chi của năm
            stem_year, branch_year = calculate_stem_and_branch_for_year(
                seen_year)

            # Cần các thông tin (thiên can, địa chi, nội quẻ, ngoại quẻ, tên quẻ)
            heavenly_by_year, earthly_by_year = compare_elements(
                year_heavenly_by_birth, year_earthly_by_birth, stem_year, branch_year)

            # Tính Nội quẻ và Ngoại quẻ
            inner_hexagram, outer_hexagram = calculate_hexagram_by_branch_birth(
                year_earthly_by_birth)

            # Xác định hào động
            active_line = determine_active_line(
                year_heavenly_by_birth, year_earthly_by_birth, stem_year, branch_year)

            # Biến đổi quẻ theo hào động
            inner_hexagram = change_hexagram_line(inner_hexagram, active_line)
            outer_hexagram = change_hexagram_line(outer_hexagram, active_line)

            shape = ''.join(inner_hexagram + outer_hexagram)
            hexagram_of_year = dict_hexagram.get(shape)

            results[seen_year] = {
                "year_heavenly_by_birth": year_heavenly_by_birth,
                "year_earthly_by_birth": year_earthly_by_birth,
                "stem_year": stem_year,
                "branch_year": branch_year,
                "heavenly_by_year": heavenly_by_year,
                "earthly_by_year": earthly_by_year,
                "inner_hexagram": inner_hexagram,
                "outer_hexagram": outer_hexagram,
                "hexagram_of_year": hexagram_of_year
            }

        # endregion

        return render_template(
            'result.html',
            name=name,
            year_of_birth=year_of_birth,
            month_of_birth=month_of_birth,
            day_of_birth=day_of_birth,
            hour_of_birth=hour_of_birth,
            heavenly_by_birth=heavenly_by_birth,
            earthly_by_birth=earthly_by_birth,
            inner_hexagram_of_birth=inner_hexagram_of_birth,
            outer_hexagram_of_birth=outer_hexagram_of_birth,
            hexagram_of_birth=hexagram_of_birth,
            year_range=year_range,
            results=results
        )

    return render_template('index.html', form=form)

# Route to handle result download


def calculate_stem_and_branch_for_year(year):
    heavenly_stem = heavenly_stems[(year - 3) % 10]
    earthly_branch = earthly_branches[(year - 3) % 12]
    return heavenly_stem, earthly_branch


def determine_active_line(stem_birth, branch_birth, stem_year, branch_year):
    # Quy tắc đơn giản để xác định hào động (có thể điều chỉnh theo logic phong thủy chi tiết hơn)
    # Nếu Thiên Can hoặc Địa Chi khắc nhau, hào sẽ động
    stem_element_birth = heavenly_stem_elements[stem_birth]
    branch_element_birth = earthly_branch_elements[branch_birth]
    stem_element_year = heavenly_stem_elements[stem_year]
    branch_element_year = earthly_branch_elements[branch_year]

    # Đơn giản hóa xác định hào động bằng cách dựa trên năm tương khắc
    if stem_element_birth != stem_element_year or branch_element_birth != branch_element_year:
        return 3  # Hào 3 động nếu có sự tương khắc (giả định đơn giản hóa)
    return 1  # Hào 1 động nếu không tương khắc

# Hàm biến đổi hào


def change_hexagram_line(hexagram, active_line):
    if active_line in [1, 2, 3]:
        hexagram[active_line - 1] = "_ _" if hexagram[active_line -
                                                      1] == "___" else "___"
    return hexagram


# Hàm luận giải tương sinh, tương khắc giữa Thiên Can, Địa Chi của năm sinh và các năm


def compare_elements(stem_birth, branch_birth, stem_year, branch_year):
    stem_element_birth = heavenly_stem_elements[stem_birth]
    branch_element_birth = earthly_branch_elements[branch_birth]
    stem_element_year = heavenly_stem_elements[stem_year]
    branch_element_year = earthly_branch_elements[branch_year]

    stem_comparison = ""
    branch_comparison = ""

    if stem_element_birth == stem_element_year:
        stem_comparison = "Thiên Can hòa hợp."
    elif stem_element_birth == "Mộc" and stem_element_year == "Thủy" or \
            stem_element_birth == "Hỏa" and stem_element_year == "Mộc" or \
            stem_element_birth == "Thổ" and stem_element_year == "Hỏa" or \
            stem_element_birth == "Kim" and stem_element_year == "Thổ" or \
            stem_element_birth == "Thủy" and stem_element_year == "Kim":
        stem_comparison = "Thiên Can sinh trợ."
    else:
        stem_comparison = "Thiên Can tương khắc."

    if branch_element_birth == branch_element_year:
        branch_comparison = "Địa Chi hòa hợp."
    elif branch_element_birth == "Mộc" and branch_element_year == "Thủy" or \
            branch_element_birth == "Hỏa" and branch_element_year == "Mộc" or \
            branch_element_birth == "Thổ" and branch_element_year == "Hỏa" or \
            branch_element_birth == "Kim" and branch_element_year == "Thổ" or \
            branch_element_birth == "Thủy" and branch_element_year == "Kim":
        branch_comparison = "Địa Chi sinh trợ."
    else:
        branch_comparison = "Địa Chi tương khắc."

    return stem_comparison, branch_comparison


if __name__ == '__main__':
    app.run(debug=True)
