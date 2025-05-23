from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional

import pandas as pd
from openpyxl.styles import PatternFill, Font, Alignment
from openpyxl.utils.dataframe import dataframe_to_rows

from ...domain.entities.author import Author
from ..queries.get_commit_statistics_query import CommitStatisticsQuery

@dataclass
class GenerateExcelReportCommand:
    """
    Command para gerar relatório Excel.
    Segue o padrão CQS (Command Query Separation).
    """
    statistics_query: CommitStatisticsQuery
    output_dir: Path
    authors: List[Author]
    
    def execute(self) -> Path:
        """
        Executa o comando para gerar o relatório Excel.
        
        Returns:
            Path: Caminho do arquivo Excel gerado
        """
        # Obtém as estatísticas
        daily_stats, monthly_stats, branch_stats = self.statistics_query.execute()
        
        if daily_stats.empty:
            raise ValueError("Nenhum dado encontrado para gerar o relatório")

        # Prepara o nome do arquivo
        timestamp = pd.Timestamp.now().strftime("%d-%m-%Y-%H-%M")
        if len(self.authors) == 1:
            author_name = self.authors[0].name.lower()
            author_name = "".join(c for c in author_name if c.isalnum() or c == '_')
        else:
            author_name = "multiple_authors"
            
        filename = f"relatorio_git_{timestamp}_{author_name}.xlsx"
        output_path = self.output_dir / filename
        
        # Garante que o diretório existe
        self.output_dir.mkdir(exist_ok=True)
        
        # Cria o arquivo Excel
        with pd.ExcelWriter(str(output_path), engine='openpyxl') as writer:
            self._create_summary_sheet(writer, daily_stats, monthly_stats, branch_stats)
            self._create_statistics_sheets(writer, daily_stats, monthly_stats, branch_stats)
            self._create_info_sheet(writer)
            self._adjust_columns(writer)
            
        return output_path
    
    def _create_summary_sheet(self, writer: pd.ExcelWriter,
                            daily_stats: pd.DataFrame,
                            monthly_stats: pd.DataFrame,
                            branch_stats: pd.DataFrame) -> None:
        """Cria a aba de resumo com todas as seções."""
        workbook = writer.book
        sheet = workbook.create_sheet('Resumo Geral')
        writer.sheets['Resumo Geral'] = sheet
        
        # Configurações de estilo
        title_font = Font(bold=True, size=12)
        section_colors = {
            'autor': 'E6F3FF',    # Azul claro
            'ambiente': 'E6FFE6',  # Verde claro
            'diario': 'FFE6E6',   # Vermelho claro
            'mensal': 'FFF3E6'    # Laranja claro
        }
        
        # Adiciona cada seção
        current_row = 1
        
        # Seção de Autores
        current_row = self._add_section(
            sheet, 'RESUMO POR AUTOR E AMBIENTE', branch_stats,
            current_row, section_colors['autor'], title_font
        )
        
        # Seção de Ambiente
        current_row = self._add_section(
            sheet, 'RESUMO POR AMBIENTE (PRD/HML)',
            self._get_environment_summary(branch_stats),
            current_row + 2, section_colors['ambiente'], title_font
        )
        
        # Seção Diária
        current_row = self._add_section(
            sheet, 'TOTAIS DIÁRIOS', daily_stats,
            current_row + 2, section_colors['diario'], title_font
        )
        
        # Seção Mensal
        self._add_section(
            sheet, 'TOTAIS MENSAIS', monthly_stats,
            current_row + 2, section_colors['mensal'], title_font
        )
    
    def _create_statistics_sheets(self, writer: pd.ExcelWriter,
                                daily_stats: pd.DataFrame,
                                monthly_stats: pd.DataFrame,
                                branch_stats: pd.DataFrame) -> None:
        """Cria as abas de estatísticas detalhadas."""
        branch_stats.to_excel(writer, sheet_name='Estatísticas por Branch', index=False)
        daily_stats.to_excel(writer, sheet_name='Estatísticas Diárias', index=False)
        monthly_stats.to_excel(writer, sheet_name='Estatísticas Mensais', index=False)
    
    def _create_info_sheet(self, writer: pd.ExcelWriter) -> None:
        """Cria a aba de informações."""
        info = pd.DataFrame([{
            'Data do Relatório': pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S"),
            'Autores': ', '.join(author.name for author in self.authors),
            'Emails': ', '.join(author.email for author in self.authors)
        }])
        info.to_excel(writer, sheet_name='Informações', index=False)
    
    def _adjust_columns(self, writer: pd.ExcelWriter) -> None:
        """Ajusta as larguras das colunas em todas as abas."""
        for sheet_name in writer.sheets:
            worksheet = writer.sheets[sheet_name]
            
            if sheet_name != 'Informações':
                # Adiciona filtros
                if worksheet.max_row > 1:
                    worksheet.auto_filter.ref = worksheet.dimensions
            
            # Ajusta larguras
            for idx, col in enumerate(worksheet.columns, 1):
                max_length = 0
                column = worksheet.column_dimensions[chr(64 + idx)]
                
                for cell in col:
                    try:
                        if len(str(cell.value)) > max_length:
                            max_length = len(str(cell.value))
                    except:
                        pass
                
                adjusted_width = (max_length + 2)
                column.width = adjusted_width
    
    def _add_section(self, sheet, title: str, data: pd.DataFrame,
                    start_row: int, color: str, title_font: Font) -> int:
        """Adiciona uma seção ao relatório com título e dados."""
        # Adiciona título
        sheet.merge_cells(f'A{start_row}:H{start_row}')
        title_cell = sheet[f'A{start_row}']
        title_cell.value = title
        title_cell.font = title_font
        title_cell.alignment = Alignment(horizontal='center')
        title_cell.fill = PatternFill(start_color=color, end_color=color, fill_type='solid')
        
        # Adiciona dados
        start_row += 1
        for r_idx, row in enumerate(dataframe_to_rows(data, index=False, header=True), start_row):
            for c_idx, value in enumerate(row, 1):
                cell = sheet.cell(row=r_idx, column=c_idx, value=value)
                if r_idx == start_row:  # Cabeçalho
                    cell.font = Font(bold=True)
                cell.fill = PatternFill(start_color=color, end_color=color, fill_type='solid')
        
        return start_row + len(data)
    
    def _get_environment_summary(self, branch_stats: pd.DataFrame) -> pd.DataFrame:
        """Gera o resumo por ambiente."""
        return branch_stats.groupby('ambiente').agg({
            'arquivos_alterados': 'sum',
            'linhas_adicionadas': 'sum',
            'linhas_removidas': 'sum',
            'total_linhas': 'sum',
            'total_commits': 'sum',
            'branch': 'nunique'
        }).reset_index().rename(columns={'branch': 'total_branches'}) 