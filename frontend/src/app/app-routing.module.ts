import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { WhiskyListComponent } from './components/whisky-list/whisky-list.component';

const routes: Routes = [
  { path: '', redirectTo: '/whiskies', pathMatch: 'full' },
  { path: 'whiskies', component: WhiskyListComponent }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }