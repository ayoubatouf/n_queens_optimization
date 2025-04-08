def generate_html_visuals(input_file, output_file, solutions_per_page=100):
    try:
        with open(input_file, "r") as in_file:
            lines = in_file.readlines()
    except FileNotFoundError:
        print(f"error: the input file '{input_file}' was not found.")
        return
    except IOError:
        print(f"error: unable to read the input file '{input_file}'.")
        return

    header_line = lines[0].strip()
    if "solutions for N=" not in header_line:
        print(
            f"error: invalid header format in input file. expected 'solutions for N=' but got: {header_line}"
        )
        return

    try:
        n = int(header_line.split("=")[1])
    except ValueError:
        print(f"error: unable to extract 'N' value from header: {header_line}")
        return

    solutions = []
    for line in lines[1:]:
        line = line.strip()
        if not line or line.isspace():
            continue

        solution = [int(x) for x in line.split()]
        if len(solution) == n:
            solutions.append(solution)

    total_solutions = len(solutions)
    if total_solutions == 0:
        print("error: no valid solutions found in the input file.")
        return

    max_allowed_solutions = 10000
    if total_solutions > max_allowed_solutions:
        print(
            f"Warning: too many solutions ({total_solutions}). Only the first {max_allowed_solutions} will be displayed."
        )
        solutions = solutions[:max_allowed_solutions]
        total_solutions = max_allowed_solutions

    total_pages = (total_solutions + solutions_per_page - 1) // solutions_per_page

    try:
        with open(output_file, "w") as out_file:

            out_file.write(
                f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>N-Queens Visuals</title>
    <style>
        body {{ 
            font-family: Arial, sans-serif; 
            margin: 20px; 
            background-color: #f4f4f4; 
        }}
        h2 {{ 
            text-align: center; 
            font-size: 32px; 
            margin-bottom: 20px; 
            color: #333; 
        }}
        .board-container {{ 
            display: flex; 
            flex-wrap: wrap; 
            justify-content: center; 
            gap: 20px; 
            margin-bottom: 30px;
        }}
        .board {{ 
            display: inline-block; 
            margin: 10px; 
            border: 2px solid #444; 
            border-radius: 8px; 
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.2); 
            transition: transform 0.3s;
        }}
        .board:hover {{
            transform: scale(1.02);
        }}
        .board h3 {{ 
            text-align: center; 
            font-size: 24px; 
            margin: 10px 0; 
        }}
        .row {{ 
            display: flex; 
        }}
        .cell {{ 
            width: 40px; 
            height: 40px; 
            box-sizing: border-box; 
            border: 1px solid #ccc; 
            text-align: center; 
            vertical-align: middle; 
        }}
        .queen {{ 
            font-size: 32px; 
            color: #000; 
        }}
        .queen:hover {{ 
            background: #ff6347; 
            transition: 0.3s; 
        }}
        .cell:hover {{ 
            cursor: pointer; 
            background-color: #ddd; 
            transition: 0.3s; 
        }}
        .white {{ 
            background-color: white; 
        }}
        .black {{ 
            background-color: #333; 
        }}
        .pagination {{
            display: flex;
            justify-content: center;
            margin: 30px 0;
            flex-wrap: wrap;
        }}
        .page-btn {{
            padding: 8px 16px;
            margin: 0 5px;
            border: 1px solid #ddd;
            background-color: #f8f8f8;
            color: #333;
            border-radius: 4px;
            cursor: pointer;
            transition: all 0.3s;
        }}
        .page-btn:hover {{
            background-color: #e7e7e7;
            border-color: #ccc;
        }}
        .page-btn.active {{
            background-color: #4CAF50;
            color: white;
            border-color: #4CAF50;
        }}
        .page-btn.disabled {{
            color: #aaa;
            cursor: not-allowed;
        }}
        .page-info {{
            text-align: center;
            margin: 20px 0;
            font-size: 18px;
            color: #555;
        }}
        .page-container {{
            display: none;
        }}
        .page-container.active {{
            display: block;
        }}
        .controls {{
            text-align: center;
            margin: 20px 0;
        }}
        .per-page-selector {{
            padding: 8px;
            border-radius: 4px;
            border: 1px solid #ddd;
        }}
    </style>
</head>
<body>
    <h2>N-Queens Visuals for N={n}</h2>
    <div class="controls">
    </div>
    <div class="page-info">Showing <span id="start-sol">1</span> to <span id="end-sol">{min(solutions_per_page, total_solutions)}</span> of <span id="total-sols">{total_solutions}</span> solutions</div>
"""
            )

            for page in range(total_pages):
                start_idx = page * solutions_per_page
                end_idx = min((page + 1) * solutions_per_page, total_solutions)

                out_file.write(
                    f'<div class="page-container" id="page-{page+1}" {"data-per-page="+str(solutions_per_page)}>'
                )
                out_file.write('<div class="board-container">')

                for i in range(start_idx, end_idx):
                    solution = solutions[i]
                    solution_num = i + 1
                    out_file.write(
                        f'<div class="board">\n<h3>Solution {solution_num}</h3>\n'
                    )

                    for row in range(n):
                        out_file.write('<div class="row">')
                        for col in range(n):
                            cell_class = "white" if (row + col) % 2 == 0 else "black"
                            if solution[col] == row:
                                out_file.write(
                                    f'<div class="cell {cell_class} queen">👑</div>'
                                )
                            else:
                                out_file.write(f'<div class="cell {cell_class}"></div>')
                        out_file.write("</div>\n")

                    out_file.write("</div>\n")

                out_file.write("</div></div>")

            out_file.write(
                f"""
    <div class="pagination">
        <button class="page-btn" onclick="changePage(1)" id="first-page">First</button>
        <button class="page-btn" onclick="changePage(currentPage-1)" id="prev-page">Previous</button>
"""
            )

            max_visible_pages = 5
            half_visible = max_visible_pages // 2

            for page in range(1, total_pages + 1):
                if (
                    total_pages <= max_visible_pages
                    or page == 1
                    or page == total_pages
                    or (page >= 1 - half_visible and page <= 1 + half_visible)
                ):
                    active = "active" if page == 1 else ""
                    out_file.write(
                        f'<button class="page-btn {active}" onclick="changePage({page})">{page}</button>'
                    )
                elif page == 2 and 1 - half_visible > 2:
                    out_file.write('<button class="page-btn disabled">...</button>')
                elif page == total_pages - 1 and 1 + half_visible < total_pages - 1:
                    out_file.write('<button class="page-btn disabled">...</button>')

            out_file.write(
                f"""
        <button class="page-btn" onclick="changePage(currentPage+1)" id="next-page">Next</button>
        <button class="page-btn" onclick="changePage({total_pages})" id="last-page">Last</button>
    </div>
"""
            )

            out_file.write(
                f"""
<script>
    let currentPage = 1;
    const totalPages = {total_pages};
    const totalSolutions = {total_solutions};
    let solutionsPerPage = {solutions_per_page};
    
    // Initialize first page
    document.getElementById('page-1').classList.add('active');
    updatePaginationControls();
    
    function changePage(page) {{
        if (page < 1 || page > totalPages || page === currentPage) return;
        
        // Hide current page
        document.getElementById(`page-${{currentPage}}`).classList.remove('active');
        
        // Show new page
        currentPage = page;
        document.getElementById(`page-${{currentPage}}`).classList.add('active');
        
        updatePaginationControls();
        updatePageInfo();
    }}
    
    function updatePaginationControls() {{
        document.getElementById('prev-page').disabled = currentPage === 1;
        document.getElementById('first-page').disabled = currentPage === 1;
        document.getElementById('next-page').disabled = currentPage === totalPages;
        document.getElementById('last-page').disabled = currentPage === totalPages;
        
        // Update active state for all page buttons
        document.querySelectorAll('.page-btn').forEach(btn => {{
            if (btn.textContent === currentPage.toString()) {{
                btn.classList.add('active');
            }} else {{
                btn.classList.remove('active');
            }}
        }});
    }}
    
    function updatePageInfo() {{
        const startSol = (currentPage - 1) * solutionsPerPage + 1;
        const endSol = Math.min(currentPage * solutionsPerPage, totalSolutions);
        document.getElementById('start-sol').textContent = startSol;
        document.getElementById('end-sol').textContent = endSol;
    }}
    
    function changePerPage() {{
        const select = document.getElementById('per-page');
        const newPerPage = parseInt(select.value);
        
        if (newPerPage === solutionsPerPage) return;
        
        solutionsPerPage = newPerPage;
        
        // Reload the page with new per-page value
        window.location.href = `${{window.location.pathname}}?per_page=${{newPerPage}}`;
    }}
    
    // Check for per_page parameter in URL
    document.addEventListener('DOMContentLoaded', function() {{
        const urlParams = new URLSearchParams(window.location.search);
        const urlPerPage = urlParams.get('per_page');
        
        if (urlPerPage) {{
            const select = document.getElementById('per-page');
            select.value = urlPerPage;
        }}
    }});
</script>
</body>
</html>
"""
            )

        print(f"HTML visualization with pagination successfully saved to {output_file}")
        print(f"total solutions: {total_solutions}")
        print(
            f"total pages: {total_pages} (with {solutions_per_page} solutions per page)"
        )

    except IOError:
        print(f"error: unable to write to output file '{output_file}'.")


generate_html_visuals("nqueens_solutions.txt", "visualization.html")
