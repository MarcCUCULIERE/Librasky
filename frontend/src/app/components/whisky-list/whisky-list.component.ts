import { Component, OnInit } from '@angular/core';
import { WhiskyService } from '../../services/whisky.service';
import { Whisky, WhiskyExport } from '../../models/whisky.model';
import { MatDialog } from '@angular/material/dialog';
import { MatSnackBar } from '@angular/material/snack-bar';
import { WhiskyFormComponent } from '../whisky-form/whisky-form.component';
import { animate, state, style, transition, trigger } from '@angular/animations';

@Component({
  selector: 'app-whisky-list',
  templateUrl: './whisky-list.component.html',
  styleUrls: ['./whisky-list.component.scss'],
  animations: [
    trigger('detailExpand', [
      state('collapsed', style({ height: '0px', minHeight: '0' })),
      state('expanded', style({ height: '*' })),
      transition('expanded <=> collapsed', animate('225ms cubic-bezier(0.4, 0.0, 0.2, 1)')),
    ]),
  ],
})
export class WhiskyListComponent implements OnInit {
  whiskies: Whisky[] = [];
  displayedColumns: string[] = ['image', 'name', 'distillery', 'type', 'age', 'country', 'personal_note', 'actions'];
  isLoading = true;
  expandedElement: Whisky | null = null;

  constructor(
    private whiskyService: WhiskyService,
    private dialog: MatDialog,
    private snackBar: MatSnackBar
  ) {}

  ngOnInit(): void {
    this.loadWhiskies();
  }

  loadWhiskies(): void {
    this.isLoading = true;
    this.whiskyService.getWhiskies().subscribe({
      next: (whiskies) => {
        this.whiskies = whiskies;
        this.isLoading = false;
      },
      error: (error: Error) => {
        console.error('Error loading whiskies:', error);
        this.showError('Erreur lors du chargement des whiskies');
        this.isLoading = false;
      }
    });
  }

  openWhiskyForm(whisky?: Whisky): void {
    const dialogRef = this.dialog.open(WhiskyFormComponent, {
      width: '600px',
      data: whisky || {}
    });

    dialogRef.afterClosed().subscribe(result => {
      if (result) {
        this.loadWhiskies();
      }
    });
  }

  deleteWhisky(id: number): void {
    if (confirm('Êtes-vous sûr de vouloir supprimer ce whisky ?')) {
      this.whiskyService.deleteWhisky(id).subscribe({
        next: () => {
          this.loadWhiskies();
          this.showSuccess('Whisky supprimé avec succès');
        },
        error: (error: Error) => {
          console.error('Error deleting whisky:', error);
          this.showError('Erreur lors de la suppression du whisky');
        }
      });
    }
  }

  exportWhiskies(): void {
    this.whiskyService.exportWhiskies().subscribe({
      next: (data: WhiskyExport) => {
        const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
        const url = window.URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.download = 'whiskies-export.json';
        link.click();
        window.URL.revokeObjectURL(url);
        this.showSuccess('Export réussi');
      },
      error: (error: Error) => {
        console.error('Error exporting whiskies:', error);
        this.showError('Erreur lors de l\'export');
      }
    });
  }

  onFileSelected(event: Event): void {
    const element = event.target as HTMLInputElement;
    const file = element.files?.[0];
    if (file) {
      this.whiskyService.importWhiskies(file).subscribe({
        next: () => {
          this.loadWhiskies();
          this.showSuccess('Import réussi');
        },
        error: (error: Error) => {
          console.error('Error importing whiskies:', error);
          this.showError('Erreur lors de l\'import');
        }
      });
    }
  }

  private showSuccess(message: string): void {
    this.snackBar.open(message, 'Fermer', {
      duration: 3000,
      panelClass: ['success-snackbar']
    });
  }

  private showError(message: string): void {
    this.snackBar.open(message, 'Fermer', {
      duration: 5000,
      panelClass: ['error-snackbar']
    });
  }
}