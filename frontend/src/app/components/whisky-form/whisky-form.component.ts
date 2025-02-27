import { Component, Inject, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';
import { WhiskyService } from '../../services/whisky.service';
import { Whisky } from '../../models/whisky.model';

@Component({
  selector: 'app-whisky-form',
  templateUrl: './whisky-form.component.html',
  styleUrls: ['./whisky-form.component.scss']
})
export class WhiskyFormComponent implements OnInit {
  whiskyForm: FormGroup;
  isEditMode: boolean = false;
  imagePreview: string | null = null;

  constructor(
    private fb: FormBuilder,
    private whiskyService: WhiskyService,
    private dialogRef: MatDialogRef<WhiskyFormComponent>,
    @Inject(MAT_DIALOG_DATA) public data: Whisky
  ) {
    this.whiskyForm = this.fb.group({
      name: ['', Validators.required],
      distillery: ['', Validators.required],
      country: ['', Validators.required],
      region: ['', Validators.required],
      age: [null],
      type: ['', Validators.required],
      personal_note: [null, [Validators.min(0), Validators.max(5)]],
      comments: [''],
      price: [null, Validators.min(0)],
      volume: [700, [Validators.required, Validators.min(0)]],
      alcohol_degree: [40, [Validators.required, Validators.min(0), Validators.max(100)]],
      image: [null],
      purchase_date: [''] // Ajout du contrôle pour la date d'achat
    });
  }

  ngOnInit(): void {
    if (this.data?.id) {
      this.isEditMode = true;
      // Si la date existe, convertissez-la en objet Date pour le datepicker
      const formData = {...this.data};
      if (formData.purchase_date) {
        formData.purchase_date = new Date(formData.purchase_date);
      }
      this.whiskyForm.patchValue(formData);
      if (this.data.image) {
        this.imagePreview = 'data:image/jpeg;base64,' + this.data.image;
      }
    }
  }

  onFileSelected(event: any): void {
    const file = event.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = () => {
        this.imagePreview = reader.result as string;
        if (this.imagePreview) {
          const base64String = this.imagePreview.split(',')[1];
          this.whiskyForm.patchValue({ image: base64String });
        }
      };
      reader.readAsDataURL(file);
    }
  }

  onSubmit(): void {
    if (this.whiskyForm.valid) {
      const whiskyData = this.whiskyForm.value;

      if (this.isEditMode) {
        this.whiskyService.updateWhisky(this.data.id!, whiskyData).subscribe({
          next: (result) => {
            this.dialogRef.close(result);
          },
          error: (error) => {
            console.error('Error updating whisky:', error);
          }
        });
      } else {
        this.whiskyService.createWhisky(whiskyData).subscribe({
          next: (result) => {
            this.dialogRef.close(result);
          },
          error: (error) => {
            console.error('Error creating whisky:', error);
          }
        });
      }
    }
  }

  onCancel(): void {
    this.dialogRef.close();
  }
}