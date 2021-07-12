import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ParcelAddComponent } from './parcel-add.component';

describe('ParcelAddComponent', () => {
  let component: ParcelAddComponent;
  let fixture: ComponentFixture<ParcelAddComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ ParcelAddComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(ParcelAddComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
