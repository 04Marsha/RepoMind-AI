import { ComponentFixture, TestBed } from '@angular/core/testing';

import { RepositoryAgent } from './repository-agent';

describe('RepositoryAgent', () => {
  let component: RepositoryAgent;
  let fixture: ComponentFixture<RepositoryAgent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [RepositoryAgent],
    }).compileComponents();

    fixture = TestBed.createComponent(RepositoryAgent);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
